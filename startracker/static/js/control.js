function Control(){

    this.getPorts = function() {
        $.get("/getPorts", function(data, status) {
            if (status === "success"){
                data = JSON.parse(data)
                dropdown = $("#select_port")
                dropdown.find("option").remove()
                data.forEach(d => {
                    dropdown.append(`<option value=${d}>${d}</option`)
                });
            } else {
                console.log(status)
                console.log(data)
            }
        })
    }

    this.connect = function() {
        port = $("#select_port").find("option:selected")[0].label
        console.log(port)
        $.get("/connect", { 'port': port }, function(data, status) {
            console.log(status)
        })
    }

    this.sendCmd = function(cmd) {
        $.get("/sendCmd", {'cmd': cmd })
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

    setInterval((function(self){return function() {self.getStatus()}})(this), 1000)
}