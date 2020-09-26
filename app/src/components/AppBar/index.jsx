import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import { useStyles } from '../styles/styles';

const BinanceAppBar = () => {
    
    const classes = useStyles();

    return (
        <AppBar position="sticky" className={classes.appbar}>
            <Toolbar>
                {/* <IconButton className={classes.menuButton}>
                    <MenuIcon />
                </IconButton> */}
                <Typography variant="h6" className={classes.title}>
                    AppName
                </Typography>
                <Button>
                    <Typography variant="button" className={classes.about}>
                        About
                    </Typography>
                </Button>
            </Toolbar>
        </AppBar>
    );
}

export default BinanceAppBar;