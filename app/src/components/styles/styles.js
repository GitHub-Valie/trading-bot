import { makeStyles } from "@material-ui/core";

export const useStyles = makeStyles({
    button: {
        backgroundColor: "red",
        '&:hover': {
            backgroundColor: 'blue',
        },
    },
    root: {
        flexGrow: 1,
    },
    title: {
        flexGrow: 1,
        color: '#FBC624'
    },
    appbar: {
        backgroundColor: "#000000"
    },
    about: {
        color: "#FBC624"
    },
    item: {
        margin: "1rem"
    },
});