import * as React from 'react';
import { createChart } from 'lightweight-charts';
import { Typography, Paper } from '@material-ui/core';
import { useStyles } from '../styles/styles';


class LightweightChart extends React.PureComponent {
    
    static defaultProps = {
		containerId: 'lightweight_chart_container',
	};

    chart = null;

    componentDidMount() {

        const chart = createChart(this.props.containerId, { width: 800, height: 300 });
        this.chart = chart;

        const lineSeries = chart.addLineSeries();
        
        lineSeries.setData([
            { time: '2019-04-10', value: 60.01 },
            { time: '2019-04-11', value: 80.01 },
        ]);

        const barSeries = chart.addBarSeries({
            thinBars: false,
        });

        // set the data
        barSeries.setData([
            { time: "2019-04-10", open: 141.77, high: 170.39, low: 120.25, close: 145.72 },
            { time: "2019-04-11", open: 145.72, high: 147.99, low: 100.11, close: 108.19 },
                 ]);
    }

	componentWillUnmount() {
		if (this.chart !== null) {
			this.chart.remove();
			this.chart = null;
		}
	}

	render() {
		return (
			<div
				id={ this.props.containerId }
                className={ 'LightweightChart' }
                style={{ margin: '1rem' }}
			/>
		);
    }
    
    // render() {
    //     return (
    //         <Paper elevation={4} style={{ margin: '1rem' }}>
    //             <Typography variant="h6">
    //                 LightweightChart
    //             </Typography>
    //         </Paper>
    //     )
    // }
}

export default LightweightChart;