from Sampling.StratifiedKFoldCrossValidation import StratifiedKFoldCrossValidation

from Classification.Experiment.Experiment import Experiment
from Classification.Experiment.KFoldRunSeparateTest import KFoldRunSeparateTest
from Classification.InstanceList.Partition import Partition
from Classification.Performance.ExperimentPerformance import ExperimentPerformance


class StratifiedKFoldRunSeparateTest(KFoldRunSeparateTest):

    def __init__(self, K: int):
        """
        Constructor for StratifiedKFoldRunSeparateTest class. Basically sets K parameter of the K-fold cross-validation.

        PARAMETERS
        ----------
        K : int
            K of the K-fold cross-validation.
        """
        super().__init__(K)

    def execute(self, experiment: Experiment) -> ExperimentPerformance:
        """
        Execute Stratified K-fold cross-validation with the given classifier on the given data set using the given
        parameters.

        PARAMETERS
        ----------
        experiment : Experiment
            Experiment to be run.

        RETURNS
        -------
        ExperimentPerformance
            An ExperimentPerformance instance.
        """
        result = ExperimentPerformance()
        instanceList = experiment.getDataSet().getInstanceList()
        partition = Partition(instanceList, 0.25, experiment.getParameter().getSeed(), True)
        crossValidation = StratifiedKFoldCrossValidation(Partition(partition.get(1)).getLists(), self.K,
                                                         experiment.getParameter().getSeed())
        self.runExperiment(experiment.getClassifier(), experiment.getParameter(), result, crossValidation,
                           partition.get(0))
        return result
