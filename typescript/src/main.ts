import 'assets/scss/app.scss'

document
    .querySelector<HTMLDivElement>('#app')!
    .innerHTML = `
<h1>Binance</h1>
<div id="chart" style="height: 400px"></div>
`
