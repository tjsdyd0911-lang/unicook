$(document).ready(function() {

    const target   = $("#recommend-data").data("target");
    const rawData  = $("#recommend-data").data("time-data"); 
    const isMember = $("#recommend-data").data("is-member") == true;

    // 메인 페이지 시간대별 분석 차트
    if(target == "main"){
        
        let similarityChart = null;
    
        $('#analysisModal').on('shown.bs.modal', function () {
            
            if (rawData.length == 0) return;
    
            // const itemNames = rawData.map(item => item.item_name); 아래 함수 선언과 같음
            var itemNames = rawData.map(function(item) {
                return item.item_name;
            });
            
            // const scores = rawData.map(item => item.score); 아래 함수 선언과 같음
            var scores = rawData.map(function(item) {
                return item.score;
            });
    
            const ctx = $("#similarityChart")[0].getContext('2d');
            if (similarityChart != null) {
                similarityChart.destroy();
            }
    
            similarityChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: itemNames,
                    datasets: [{
                        label: isMember ? '취향 매칭 점수' : '실시간 인기 점수',
                        data: scores,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.6)',
                            'rgba(54, 162, 235, 0.6)',
                            'rgba(255, 206, 86, 0.6)',
                            'rgba(75, 192, 192, 0.6)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)'
                        ],
                        borderWidth: 1,
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend:  { display: false },
                        tooltip: { 
                            callbacks: {
                                label: function(context) {
                                        return ' 매칭 점수: ' + (context.raw * 100).toFixed(1) + '%';
                                       }       
                            }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            max: 1.0,
                            grid: { display: false },
                            ticks: {
                                callback: function(value) { return (value * 100) + '%'; }
                            }
                        },
                        y: {
                            ticks: {
                                font: { size: 11 }
                            }
                        }
                    }
                }
            });
    
            if (isMember && scores.length > 0) {
            
                // const avg = (scores.reduce((a, b) => a + b, 0) / scores.length) * 100; 아래 함수와 같음
                var sum = scores.reduce(function(a, b) {
                    return a + b;
                }, 0);
                var avg = (sum / scores.length) * 100;
                
                $('#avg-score-display').text(avg.toFixed(1));
            }
        });
    }
});