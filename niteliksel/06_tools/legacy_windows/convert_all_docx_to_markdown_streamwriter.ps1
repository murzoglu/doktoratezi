$outputFile = "tum_dokumler.md"
$docxFiles = Get-ChildItem *.docx

Write-Host "Starting conversion of $( $docxFiles.Count ) files using StreamWriter..."

# Use StreamWriter for efficient and exclusive write access
try {
    $sw = [System.IO.StreamWriter]::new($outputFile, $false, [System.Text.Encoding]::UTF8)
}
catch {
    Write-Error "Could not open $outputFile for writing. Is it open in another program?"
    exit
}

try {
    foreach ($file in $docxFiles) {
        Write-Host "Processing $($file.Name)..."
        $sw.WriteLine("# $($file.Name)")
        $sw.WriteLine("")

        $tempDir = Join-Path $env:TEMP "docx_convert_$($file.BaseName)_$(Get-Random)"
        New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

        try {
            # Copy to zip
            $zipPath = Join-Path $tempDir "content.zip"
            Copy-Item -LiteralPath $file.FullName -Destination $zipPath

            $extractDir = Join-Path $tempDir "extracted"
            Expand-Archive -Path $zipPath -DestinationPath $extractDir -Force

            $xmlPath = Join-Path $extractDir "word\document.xml"
            if (Test-Path $xmlPath) {
                [xml]$xml = Get-Content $xmlPath
                $nsManager = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
                $nsManager.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")

                $nodes = $xml.SelectNodes("//w:p", $nsManager)
                foreach ($node in $nodes) {
                    $textNodes = $node.SelectNodes(".//w:t", $nsManager)
                    if ($textNodes) {
                        $text = ($textNodes | ForEach-Object { $_.InnerText }) -join ""
                        if (-not [string]::IsNullOrWhiteSpace($text)) {
                            $sw.WriteLine($text)
                            $sw.WriteLine("")
                        }
                    }
                }
            } else {
                $sw.WriteLine("> Error: Invalid DOCX structure (missing document.xml)")
            }
        }
        catch {
            Write-Host "Error converting $($file.Name): $_"
            $sw.WriteLine("> Error converting file: $_")
        }
        finally {
            Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
        }

        $sw.WriteLine("---")
        $sw.WriteLine("")
    }
}
finally {
    $sw.Close()
    $sw.Dispose()
    Write-Host "File closed."
}

Write-Host "Conversion complete. Saved to $outputFile"
