const express = require('express');
const app = express();
const path = require('path');
const mongoose = require('mongoose')

try {
    mongoose.connect('mongodb://localhost:27017/concreteMix');
} catch (err) {
    console.log('Not Connected to Database');
}

// Schemas
const Mix = require('./models/Mix');
const Supplier = require('./models/Supplier');

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');


app.get('/drift_analysis', (req, res) => {
    res.render("drift_analysis")
})

// app.get('/suppliers', (req, res) => {
//     res.render('suppliers/index')
// })

// app.get('/suppliers/new', (req, res) => {
//     res.render('suppliers/new')
// })

// app.get('/mixes', (req, res) => {
//     res.render('mixes/index')
})

app.listen(3000, () => {
    console.log('Connected to port 3000');
})