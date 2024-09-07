function Control(){

    $("#bearing_range").on("change", function() {
        $("#in_bearing").val($("#bearing_range").val())
    });

    $("#azimuth_range").on("change", function() {
        $("#in_azimuth").val($("#azimuth_range").val())
    });

    this.getPorts = function() {
        $.get("/getPorts", function(data, status) {
            if (status === "success"){
                data = JSON.parse(data)
                dropdown = $("#select_port")
                dropdown.find("option").remove()
                data.forEach(d => {
                    dropdown.append(`<option value=${d}>${d}</option>`)
                });
            } else {
                console.log(status)
                console.log(data)
            }
        })
    }

    this.connect = function() {
        port = $("#select_port").find("option:selected")[0].label
        $.get("/connect", { 'port': port })
    }

    this.disconnect = function() {
        $.get("/disconnect")
    }

    this.sendCmd = function(cmd) {
        $.get("/sendCmd", {'cmd': cmd + "\n" })
    }

    this.sendData = function(cmd) {
        $.get("/sendData", {'cmd': cmd + "\n" })
    }

    this.getStatus = function() {
        $.get("/status", function(data, status) {
            data = JSON.parse(data)
            if(status === "success"){
                $("#bearing").html(data["Be"])
                $("#azimuth").html(data["Az"])
            }
        })
    }

    this.jog = function(x, y){
        cmd = "JOG," + x + "," + y;
        this.sendCmd(cmd)
    }

    this.setPole = function() {
        this.sendCmd("SET_POLE,N");
    }

    this.fixPosition = function() {
        this.sendCmd("FIX");
    }

    this.btn_moveTo = function(x, y) {
        x = $("#in_bearing").val()
        y = $("#in_azimuth").val()
        this.moveTo(x, y)
    }

    this.moveTo = function(x, y) {
        cmd = "MOVE," + x + "," + y;
        this.sendCmd(cmd)
    }

    this.trackObject = function(){
        id = $("#select_object").find("option:selected").val()
        $.get("/track", 
            { "ID": id }
        )
    }

    this.quickTrack = function(){
        id = $("#catno").val()
        $.get(`https://celestrak.org/NORAD/elements/gp.php?CATNR=${id}&FORMAT=tle`, function(data, status){
            if (status == "success"){
                satData = data.split("\r\n")
                satData = {
                    "Name": satData[0].trim(),
                    "tle1": satData[1],
                    "tle2": satData[2],
                }
                $.get("/setTLE", satData)
            }
        })
    }

    this.setMode = function(){
        state = $("#mode_switch").is(":checked")
        state = state ? 1 : 0
        this.sendData(`MODE,${state}\n`);
    }
    

    // setInterval((function(self){return function() {self.getStatus()}})(this), 1000)
}