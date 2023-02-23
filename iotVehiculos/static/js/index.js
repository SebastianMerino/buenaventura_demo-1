document.addEventListener('DOMContentLoaded',()=>{
    let tablaVendedor = new Chart(document.getElementById('grafEncendido'),{
        type:'line',
        options:{
            scales:{
                x:{
                    grid:{
                        display: false,
                    },
                    type: 'time',
                    time: {
                        unit: 'minute'
                    }
                },
                y:{
                    max:1.5,
                    min:-0.5,
                    grid:{
                        display: false,
                    },
                    ticks: {
                        callback: function(val) {
                            if (val==1)
                                return "ON";
                            else if (val==0)
                                return "OFF";
                        },                
                    }
                },
            },
        },
        data:{
            labels:[],
            datasets:[{
                label:'Encendido del vehiculo',
                backgroundColor:'#008CBA',
                //backgroundColor: Utils.CHART_COLORS.blue,
                borderColor: '#008CBA',
                pointRadius: 0,
                data:[],
            }]
        }
    })

    setInterval(()=>{
        fetch('/iotVehiculos/enviarDatos?cantidad=40')
        .then(response=>response.json())
        .then(data => {
            console.log(data)
            tablaVendedor.data.labels = data.registroTiempos
            tablaVendedor.data.datasets[0].data = data.informacionVehiculo
            tablaVendedor.update()
        })
    },1000)
})