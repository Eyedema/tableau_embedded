// Initialize the viz variable 
var viz;


window.onload = function() {
// When the webpage has loaded, load the viz
    var vizDiv = document.getElementById('myViz');
    var vizUrl = "https://public.tableau.com/views/SuperSampleSuperstore/SuperDescriptive";
    var options = {
        height: 830,
        width: 1024,
        hideToolbar: true,
        hideTabs: false
    }
    viz = new tableau.Viz(vizDiv, vizUrl, options);
}

// Switch the viz to the sheet specified
function switchView(sheetName) {
    var workbook = viz.getWorkbook();
    workbook.activateSheetAsync(sheetName);
}

// Filter the specified dimension to the specified value(s)
function show(filterName, values) {
    var sheet = viz.getWorkbook().getActiveSheet();
    if(sheet.getSheetType() === tableau.SheetType.WORKSHEET) {
        sheet.applyFilterAsync(filterName, values, tableau.FilterUpdateType.REPLACE);
    } else { // We know sheet.getSheetType() === tableau.SheetType.DASHBOARD
        var worksheetArray = sheet.getWorksheets();
		for(var i = 0; i < worksheetArray.length; i++) {
			worksheetArray[i].applyFilterAsync(filterName, values, tableau.FilterUpdateType.REPLACE);
		}
    }
}

// Select the marks that have the specified value(s) for the specified dimension
function exportPDF() {
    viz.showExportPDFDialog();
}

function resetViz(){
    var workbook = viz.getWorkbook();
    workbook.revertAllAsync();
}
