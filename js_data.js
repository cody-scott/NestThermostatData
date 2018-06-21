var outtxt = "";
var base = $$("tr.day-row.open.expandable");
for (var bi = 0; bi<base.length; bi++) {
    var bm = base[bi];
    var day = bm.querySelector(".day-label").children[0].innerText;
    var x = bm.querySelector(".usage").querySelectorAll(':scope > .usage-period.cool-light');
    var z = [];
    for (var i=0; i<x.length; i++) {
        var w = parseFloat(x[i].style.width)/100;
        var l = parseFloat(x[i].style.left)/100;
        z.push([l, w]);
    }    
    outtxt += "\n";
    outtxt += day + "\n";
    for (var i=0; i<z.length; i++) {
        outtxt += z[i][0] + "\t" + z[i][1] + "\n";
    }
    console.log(day + "\n")
    console.log(JSON.stringify(z))
}
