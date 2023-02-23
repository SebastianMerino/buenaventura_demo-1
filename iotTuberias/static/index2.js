document.addEventListener('DOMContentLoaded',()=>{
    let tablaVendedor = new Chart(document.getElementById('grafCaudal'),{
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
                    },
                },
                y:{
                    min:0,
                    max:100,
                    grid:{
                        display: false,
                    },
                },
            },
        },
        data:{
            labels:[],
            datasets:[{
                label:'Caudal de la tuberia',
                backgroundColor:'#008CBA',
                //backgroundColor: Utils.CHART_COLORS.blue,
                borderColor: '#008CBA',
                pointRadius: 0,
                data:[],
            }]
        }
    })

    setInterval(()=>{
        fetch('/iotTuberias/enviarDatos?cantidad=40')
        .then(response=>response.json())
        .then(data => {
            console.log(data)
            tablaVendedor.data.labels = data.registroTiempos
            tablaVendedor.data.datasets[0].data = data.informacionTuberia
            tablaVendedor.update()
        })
    },5000)
})