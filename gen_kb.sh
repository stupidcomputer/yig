files=$(find kb -type f | awk -F'/' '{print $NF}')
IFS='
'
mkdir -p franklincce/staticfiles/kb

for file in $files; do
  	without_extension=${file%.*}
    echo $file, $without_extension
    pandoc -s --template=./template.html -f markdown -t html -o "franklincce/staticfiles/kb/$without_extension.html" "kb/$without_extension.md" --lua-filter=links-to-html.lua
done