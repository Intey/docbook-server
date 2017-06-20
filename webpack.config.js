var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

// yo dawg i heard you like configs so we put a config in yo config so you can
// config when you config.
var DEV_ENV = process.env.DEV;
var DEV = (!DEV_ENV || DEV_ENV === "")

var config = {
context: path.resolve(__dirname, './js/'),

entry: {
    index:  ['index.js']
},
output: {
    path: path.resolve(__dirname, './static'),
    filename: '[name].js', // use entry field name.
    // for hot reload.
    publicPath: DEV ? 'http://localhost:3000/static/' : '/static/js/',
    library: 'lib' // for inlined JS in HTML.
},

module: {
    rules: [
        // to transform JSX into JS
        {
            test: [/\.js?$/, /\.jsx?$/],
            exclude: /node_modules/,
            loader: 'babel-loader',
            query: {
                presets: ['es2015', 'react', 'stage-0']
            },
            //ignore, couze we have above query and babelrc used by mocha
            // babelrc: false,

        },
    ],
    loaders: {}
},

resolve: {
    modules: [
        path.join(__dirname, "js/"),
        "node_modules"
    ]
},

plugins: [
    // no genereta empty output, if errors occur
    new webpack.NoEmitOnErrorsPlugin(),
    // integration with django
    new BundleTracker({filename: "./webpack-stats.json"}),
    // for bootstrap.js in node_modules
    new webpack.ProvidePlugin({ jQuery: 'jquery', }),
],


}

var plugins = [];
var loaders = [];

// diff between dev & prod.
if (DEV) {
    loaders.push(
        { // hope that order not does not affect
            test: [/\.js?$/, /\.jsx?$/],
            exclude: /node_modules/,
            loader: 'react-hot'
        }
    );

    config.devtool = 'source-map';
}

else {
    plugins.push(
        new webpack.optimize.UglifyJsPlugin({
            compress: { warnings: false },
            // prevent renaming(mangling) this vars
            mangle: { except: ['$super', '$', 'exports', 'require'] },
            sourceMap: false // on circleCI it's throw error from UglifyJsPlugin
        })
    );
}

config.plugins = config.plugins.concat(plugins);
// prepending, because order is affects
config.module.loaders = loaders.concat(config.module.loaders);

module.exports = config;
