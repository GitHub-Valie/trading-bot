import React from 'react';
import BinanceAppBar from "./components/AppBar/index";
import LightweightChart from "./components/Chart/index";
import WalletStatus from "./components/WalletStatus/index";
import OrderHistory from "./components/OrderHistory/index";
import { Grid } from '@material-ui/core'
import { useStyles } from './components/styles/styles';

function App() {
    const classes = useStyles();
    return (
        <Grid container spacing={2}>
            <Grid item lg={12}>
                <BinanceAppBar/>
            </Grid>
            <Grid item lg={9}>
                <LightweightChart/>
            </Grid>
            <Grid item lg={3}>
                <WalletStatus/>
            </Grid>
            <Grid item lg={12}>
                <OrderHistory/>
            </Grid>
        </Grid>
    );
}

export default App;