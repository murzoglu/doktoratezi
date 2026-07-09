$outputFile = "tum_dokumler.md"
$docxFiles = Get-ChildItem *.docx

Write-Host "Starting conversion of $( $docxFiles.Count ) files..."
"" | Set-Content -Path $outputFile -Encoding UTF8

foreach ($file in $docxFiles) {
    Write-Host "Processing $($file.Name)..."
    "# $($file.Name)" | Add-Content -Path $outputFile -Encoding UTF8
    "" | Add-Content -Path $outputFile -Encoding UTF8

    # Create a robust temp path in the user's temp folder
    $tempDir = Join-Path $env:TEMP "docx_convert_$($file.BaseName)_$(Get-Random)"
    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

    try {
        # Copy to a zip file extension so Expand-Archive treats it correctly
        $zipPath = Join-Path $tempDir "content.zip"
        Copy-Item -LiteralPath $file.FullName -Destination $zipPath

        $extractDir = Join-Path $tempDir "extracted"
        # Expand-Archive is standard in PS 5+ (Windows 10/11)
        Expand-Archive -Path $zipPath -DestinationPath $extractDir -Force

        $xmlPath = Join-Path $extractDir "word\document.xml"
        if (Test-Path $xmlPath) {
            # XML Parsing
            [xml]$xml = Get-Content $xmlPath
            $nsManager = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
            $nsManager.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")

            # Select paragraphs
            $nodes = $xml.SelectNodes("//w:p", $nsManager)
            foreach ($node in $nodes) {
                # Extract text from run nodes (w:t)
                # Note: This is a basic extraction. It ignores complex formatting but gets the text.
                $textNodes = $node.SelectNodes(".//w:t", $nsManager)
                if ($textNodes) {
                    $text = ($textNodes | ForEach-Object { $_.InnerText }) -join ""
                    if (-not [string]::IsNullOrWhiteSpace($text)) {
                        $text | Add-Content -Path $outputFile -Encoding UTF8
                        "" | Add-Content -Path $outputFile -Encoding UTF8
                    }
                }
            }
        } else {
            Write-Warning "Could not find word/document.xml in $($file.Name)"
            "> Error: Invalid DOCX structure" | Add-Content -Path $outputFile -Encoding UTF8
        }
    }
    catch {
        Write-Host "Error converting $($file.Name): $_"
        "> Error converting file: $_" | Add-Content -Path $outputFile -Encoding UTF8
    }
    finally {
        # Clean up temp files
        Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }

    "---" | Add-Content -Path $outputFile -Encoding UTF8
    "" | Add-Content -Path $outputFile -Encoding UTF8
}

Write-Host "Conversion complete. Output saved to $outputFile"
