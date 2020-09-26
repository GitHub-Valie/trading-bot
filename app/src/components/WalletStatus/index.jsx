import React from 'react';
import { useStyles } from '../styles/styles';
import Paper from '@material-ui/core/Paper';
import { Typography } from '@material-ui/core';

const WalletStatus = () => {                // On déclare le composant et ses props (entre les parenthèses)
    const classes = useStyles()             // classes contient la fonction useStyles
    
    return (
        <Paper elevation={4} className={classes.item}>
            <Typography variant="h6">
                WalletStatus
            </Typography>
        </Paper>
    );                               // return va retourner l'affichage, on y fait appel aux fonctions via les variables        
}

export default WalletStatus;