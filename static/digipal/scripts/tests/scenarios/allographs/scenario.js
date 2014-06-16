function Scenario() {

    var Scenarios = function(AnnotatorTasks, options) {

        var tasks = require('./actions.js').Actions(options);

        /*
        - @Scenario1
        - Select any graph
        - Make sure a popup comes out, displaying correct component and features
        - Make sure the checked feature appears into the summary popup on the left side of the popup
        - Check any feature, make sure it appears in the summary popup. Then uncheck it again, and make sure it disappears from the summary popup.
        */

        this.Scenario1 = function() {
            casper.echo('Running Allographs Scenario 1', 'PARAMETER');
            if (tasks.tabs.current() !== '#allographs') {
                tasks.tabs.switch('allographs');
            }
            casper.wait(300);

            // waiting for 300 ms as the animation makes the page still invisible for
            // a brief fraction of time
            //

            var feature = tasks.get.random_vector();
            tasks.do.select(feature, function() {
                tasks.dialog.doesDialogExist();
                tasks.dialog.doesSummaryExist();
                tasks.dialog.labelMatchesForm();
                var graph = AnnotatorTasks.get.getGraphByVectorId(feature);
                var features = AnnotatorTasks.dialog.getSelectedFeatures('allographs');
                AnnotatorTasks.tests.dialogMatchesCache(features, 'allographs', graph);
                AnnotatorTasks.do.describe('allographs');
                tasks.tests.summaryMatchesCheckboxes();
                console.log('Deselecting some checkboxes and repeating test ...');
                AnnotatorTasks.do.describe('allographs', false);
                tasks.tests.summaryMatchesCheckboxes();
            });
        };

        /*
        - Replicate the same actions of the annotator tab
        - Selecting and saving annotations
        - Deselecting all annotations
        - Selecting and removing annotations
     */

        this.Scenario2 = function() {
            casper.echo('Running Allographs Scenario 2', 'PARAMETER');

            var feature = tasks.get.random_vector();
            AnnotatorTasks.do.describeForms('allographs');
            casper.wait(600);
            tasks.do.select(feature, function() {

                casper.then(function() {
                    tasks.do.save(function() {
                        tasks.do.deselect_all_graphs();
                        casper.evaluate(function() {
                            return $('#status').remove();
                        });
                        feature = tasks.get.random_vector();
                        tasks.do.select(feature, function() {
                            tasks.do.delete();
                        });
                    });
                });
            });
        };

        /*
        - Select multiple graphs
        - Try to delete them and make sure they actually disappear form the page
         */

        this.Scenario3 = function() {
            casper.echo('Running Allographs Scenario 3', 'PARAMETER');

            var feature = tasks.get.random_vector();
            var feature2 = tasks.get.random_vector();

            casper.then(function() {
                tasks.do.select(feature);
            });

            casper.then(function() {
                tasks.do.select(feature2);
            });

            casper.then(function() {
                tasks.do.delete(function() {
                    casper.test.assertDoesntExist(x('.annotation_li[@data-annotation="' + feature + '"]'), 'Feature has been deleted');
                    casper.test.assertDoesntExist(x('.annotation_li[@data-annotation="' + feature + '"]'), 'Feature 2 has been deleted');
                });
            });
        };

    };

    this.init = function(options) {
        var AnnotatorActions = require('../annotator/actions.js').Actions(options);
        AnnotatorActions.get.adminAccess(options.page + '/admin', casper.cli.get('username'), casper.cli.get('password'))
            .then(function() {
                var scenarios = new Scenarios(AnnotatorActions, options);
                var scenariosList = [];
                for (var i in scenarios) {
                    scenariosList.push(scenarios[i]);
                }
                casper.eachThen(scenariosList, function(response) {
                    response.data.call();
                });
            });
    };

}


exports.AllographsTest = new Scenario();