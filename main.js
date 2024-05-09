var {pdfjsLib} = globalThis;

function concatLines(lines) {
    output = "";
    for (var line = 0; line < lines.length; line++) {
        output += lines[line].str;
    }
    return output;
}

function fillInCommitteePages(pages) { // TODO: make this more efficent
    output = []
    for(var i = pages[0]; i < pages[pages.length - 1]; i++) {
        if (!pages.includes(i)) output.push(i)
    }
    return output
}

function concatAllCommitteePages(committeePages, allLines) {
    output = []
    for (var i = 0; i < committeePages.length; i++) {
        output = output.concat(allLines[committeePages[i]])
    }
    return output;
}

function splitByBillHeader(committeeLines, billHeader) {
    output = [];
    current = [];
    for (var i = 0; i < committeeLines.length; i++) {
        if(committeeLines[i].str == billHeader) {
            output.push(current);
            current = [];
        } else {
            current.push(committeeLines[i])
        }
    }
    output.shift()
    return output;
}

function extractBillInformation(splittedByBillHeader) {
    var output = [];
    for (var i = 0; i < splittedByBillHeader.length; i++) {
        current = splittedByBillHeader[i];
        console.log(current)
        var subcommittee = current[31].str;
        var sponsors = current[33].str;
        var school = current[35].str;
        var billcode = current[5].str;

        output.push({
            subcommittee: subcommittee,
            sponsors: sponsors,
            school: school,
            billcode: billcode,
        })
    }

    return output;
}

function processLines(lines) {
    var committeePages = [];
    var endPage = null;
    for (var i = 0; i < lines.length; i++) {
        var concatted = concatLines(lines[i])
        if (concatted.includes("COMMITTEE") && concatted.includes("GOVERNMENT")) { // we have a committee page
            committeePages.push(i)
        } else if (concatted.includes("ABCs")) {
            endPage = i;
        }
    }
    committeePages.push(endPage)
    committeeLines = 
        concatAllCommitteePages(
            fillInCommitteePages(
                committeePages
            ), lines
        )
    
    billHeader = committeeLines[0].str;
    committeeLines.push({str: billHeader})

    splittedByBillHeader = splitByBillHeader(committeeLines, billHeader)
    billInfo = extractBillInformation(splittedByBillHeader);
    console.log(billInfo)
}

function onFileUpload() {
    const reader = new FileReader()
    var result = null;
    reader.onload = function(evt) {
        const contents = evt.target.result;
        pdfjsLib.GlobalWorkerOptions.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.mjs';
        var task = pdfjsLib.getDocument({data: contents});
        var result = task.promise.then(function(pdf) {
            var pageCount = pdf.numPages;
            var promises = [];
            for (var i = 1; i <= pageCount; i++) {
                var page = pdf.getPage(i);
                promises.push(page.then(function(page) {
                    var textContent = page.getTextContent();
                    return textContent.then(function(text) {
                        return text.items;
                    })
                }))
            }
            Promise.all(promises).then(function(lines) {
                processLines(lines)
            })
        })
    }

    reader.readAsBinaryString(document.getElementById("fileupload").files[0])
}