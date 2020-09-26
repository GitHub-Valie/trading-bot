import React from 'react';
import Paper from '@material-ui/core/Paper';
import { useStyles } from '../styles/styles';
import { Typography } from '@material-ui/core';

const OrderHistory = () => {
    const classes = useStyles()

    return (
        <Paper elevation={4} className={classes.item}>
            <Typography variant="h6">
                OrderHistory
            </Typography>
        </Paper>
    )
}

export default OrderHistory;