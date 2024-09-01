
function lookupID(noradID){
    $.get(`https://celestrak.org/NORAD/elements/gp.php?CATNR=${noradID}&FORMAT=tle`, function(data, status){
        if (status == "success"){
            satData = data.split("\r\n")
            satData = {
                "Name": satData[0].trim(),
                "tle1": satData[1],
                "tle2": satData[2],
            }
            console.log(satData)
            fill(satData)
        }
    })
}

function lookupFreq(noradID){
    $.get(`https://www.n2yo.com/satellite/?s=${noradID}`, function(data, status){
        if (status == "success"){
            radioData = $(data).find('div:contains("Uplink")')
            console.log(radioData) 
        }
    })
}

function fill(data){
    $("#name").val(data.Name)
    $("#tle1").val(data.tle1)
    $("#tle2").val(data.tle2)
}

function autofill() {
    noradID = $("#noradID").val()
    lookupID(noradID)
    lookupFreq(noradID)
}