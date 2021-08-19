<script>
    extraversion_count = parseInt("{{parameter_count_1.Extraversion}}");
    sensing_count = parseInt("{{parameter_count_1.Sensing}}");
    thinking_count = parseInt("{{parameter_count_1.Thinking}}");
    judgement_count = parseInt("{{parameter_count_1.Judgement}}");
    introversion_count = parseInt("{{parameter_count_2.Introversion}}");
    intuition_count = parseInt("{{parameter_count_2.Intuition}}");
    feeling_count = parseInt("{{parameter_count_2.Feeling}}");
    perception_count = parseInt("{{parameter_count_2.Perception}}");
    var ctx = document.getElementById('myChart');
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Extraversion', 'Sensing', 'Thinking', 'Judgement'],
        datasets: [{
          label: 'Strong traits',
          data: [extraversion_count / (extraversion_count + introversion_count),
          sensing_count / (sensing_count + intuition_count),
          thinking_count / (thinking_count + feeling_count),
          judgement_count / (judgement_count + perception_count)
          ],
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
          ],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
    var introversion_chart = document.getElementById('piechart1');
    var pie1 = new Chart(introversion_chart, {
      type: 'pie',
      data: {
        labels: [
          'Introversion',
          'Extraversion',
        ],
        datasets: [{
          label: 'Introversion',
          data: [introversion_count, extraversion_count],
          backgroundColor: [
            'rgb(255, 0, 0)',
            'rgb(255, 255, 255)',

          ],
          hoverOffset: 4
        }]
      }
    }
    )
    var intuition_chart = document.getElementById('piechart2');
    var pie2 = new Chart(intuition_chart, {
      type: 'pie',
      data: {
        labels: [
          'Intuition',
          'Sensing',
        ],
        datasets: [{
          label: 'Intuition',
          data: [intuition_count, sensing_count],
          backgroundColor: [
            'rgb(255, 0, 0)',
            'rgb(255,255,255)',
          ],
          hoverOffset: 4
        }]
      }
    }
    )
    var feeling_chart = document.getElementById('piechart3');
    var pie3 = new Chart(feeling_chart, {
      type: 'pie',
      data: {
        labels: [
          'Feeling', 'Thinking',
        ],
        datasets: [{
          label: 'Feeling',
          data: [feeling_count, thinking_count],
          backgroundColor: [
            'rgb(255, 0, 0)',
            'rgb(255,255,255)',
          ],
          hoverOffset: 4
        }]
      }
    }
    );
    var perception_chart = document.getElementById('piechart4');
    var pie4 = new Chart(perception_chart, {
      type: 'pie',
      data: {
        labels: [
          'Perception', 'Judgement',
        ],
        datasets: [{
          label: 'Perception',
          data: [perception_count, judgement_count],
          backgroundColor: [
            'rgb(255, 0, 0)',
            'rgb(255,255,255)',

          ],
          hoverOffset: 4
        }]
      }
    }
    );
    var introversion_chart2 = document.getElementById('linechart1');
    var line1 = new Chart(introversion_chart2, {
      type: 'line',
      data: {
        labels: ['a','b'],
        datasets: [{
          label: 'My First Dataset',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      }
    });
</script>