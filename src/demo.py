import optuna as optuna
import sys
import os
print("Hello world")
def objective(trial):
  x = trial.suggest_float("x", 0, 10)
  return x ** 2
if __name__ == "__main__":
  os.chdir("../../../")
  print(os.getcwd())
  path = os.getcwd()+sys.argv[1]
  #study = optuna.create_study(storage="sqlite:///LAI.db", study_name="LAIndex", direction="minimize")
  #study = optuna.create_study(storage="sqlite:///PV.db", study_name="perfvar", direction="minimize")
  study = optuna.create_study(storage=f"{path}sqlite:///CG.db", study_name="cg", direction="minimize")
  study = optuna.create_study(storage=f"{path}sqlite:///LU.db", study_name="lu", direction="minimize")
  study = optuna.create_study(storage=f"{path}sqlite:///FT.db", study_name="ft", direction="minimize")
  study = optuna.create_study(storage=f"{path}sqlite:///MG.db", study_name="mg", direction="minimize")
  study = optuna.create_study(storage=f"{path}sqlite:///KRIPKE.db", study_name="kripke", direction="minimize")
  study = optuna.create_study(storage=f"{path}sqlite:///AMR.db", study_name="amr", direction="minimize")
  #study = optuna.create_study(storage="sqlite:///hypre.db", study_name="hypreREG", direction="minimize")
  #study = optuna.create_study(storage="sqlite:///mi50.db", study_name="mi50REG", direction="minimize")
  #study = optuna.create_study(storage="sqlite:///TB.db", study_name="TBREG", direction="minimize")
  #study = optuna.create_study(storage="sqlite:///PS.db", study_name="PSREG", direction="minimize")
  #study = optuna.create_study(storage="sqlite:///TS.db", study_name="TSREG", direction="minimize")
  #study = optuna.create_study(storage="sqlite:///PB.db", study_name="PBREG", direction="minimize")
  """
  study = optuna.create_study(storage="sqlite:///ResidualStudy.db", study_name="RESFOR_PS-5-0", direction="minimize")
  study = optuna.create_study(storage="sqlite:///ResidualStudy.db", study_name="RESFOR_PS-5-1", direction="minimize")
  study = optuna.create_study(storage="sqlite:///ResidualStudy.db", study_name="RESFOR_PS-5-2", direction="minimize")
  """
  #study = optuna.create_study(storage="sqlite:///LFStudy.db", study_name="LF_FOR-PB", direction="minimize")
  #study = optuna.create_study(storage="sqlite:///FinalStudy.db", study_name="Final_FOR-PB", direction="minimize")
  #study = optuna.create_study(storage="sqlite:///LFStudy.db", study_name="LF_FOR-PB", direction="minimize")
  #study = optuna.create_study(storage="sqlite:///LFStudy.db", study_name="LF_FOR-5-2", direction="minimize")
#study = optuna.create_study(storage="sqlite:///PBIPT2.db", study_name="IPTFOR_TB-5-0", direction="minimize")
#study = optuna.create_study(storage="sqlite:///PBIPT2.db", study_name="IPTFOR_TB-5-1", direction="minimize")
#study = optuna.create_study(storage="sqlite:///PBIPT2.db", study_name="IPTFOR_TB-5-2", direction="minimize")

"""
study = optuna.create_study(storage="sqlite:///PBIPT3.db", study_name="IPTFOR_PS-15-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PBIPT3.db", study_name="IPTFOR_PS-15-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PBIPT3.db", study_name="IPTFOR_PS-15-2", direction="minimize")

#study = optuna.create_study(storage="sqlite:///PBIPT4.db", study_name="IPTFOR_PS-20-0", direction="minimize")
#study = optuna.create_study(storage="sqlite:///PBIPT4.db", study_name="IPTFOR_PS-20-1", direction="minimize")
#study = optuna.create_study(storage="sqlite:///PBIPT4.db", study_name="IPTFOR_PS-20-2", direction="minimize")

#study = optuna.create_study(storage="sqlite:///PBIPT5.db", study_name="IPTFOR_PS-25-0", direction="minimize")
#study = optuna.create_study(storage="sqlite:///PBIPT5.db", study_name="IPTFOR_PS-25-1", direction="minimize")
#study = optuna.create_study(storage="sqlite:///PBIPT5.db", study_name="IPTFOR_PS-25-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///PBIPT2.db", study_name="IPTFOR_PS-10-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PBIPT2.db", study_name="IPTFOR_PS-10-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PBIPT2.db", study_name="IPTFOR_PS-10-2", direction="minimize")
"""
"""
study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-5-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-5-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-5-2", direction="minimize")


study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-15-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-15-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-15-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-20-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-20-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-20-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-25-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-25-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-25-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-10-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-10-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT2.db", study_name="IPTFOR_PB-10-2", direction="minimize")
"""

"""
study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-5-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-5-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-5-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-10-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-10-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-10-2", direction="minimize")


study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-25-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-25-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-25-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-20-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-20-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-20-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-15-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-15-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT22.db", study_name="SUBFOR_PB-15-2", direction="minimize")





study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-5-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-5-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-5-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-10-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-10-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-10-2", direction="minimize")


study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-15-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-15-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-15-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-20-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-20-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-20-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-25-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-25-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///PSIPT222.db", study_name="REGFOR_PB-25-2", direction="minimize")
"""




"""
study = optuna.create_study(storage="sqlite:///basic_lstm100IPT1.db", study_name="IPTFOR_basic_lstm50-5-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm100IPT1.db", study_name="IPTFOR_basic_lstm50-5-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm100IPT1.db", study_name="IPTFOR_basic_lstm50-5-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///basic_lstm100IPT2.db", study_name="IPTFOR_basic_lstm50-10-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm100IPT2.db", study_name="IPTFOR_basic_lstm50-10-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm100IPT2.db", study_name="IPTFOR_basic_lstm50-10-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///basic_lstm100IPT3.db", study_name="IPTFOR_basic_lstm50-15-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm100IPT3.db", study_name="IPTFOR_basic_lstm50-15-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm100IPT3.db", study_name="IPTFOR_basic_lstm50-15-2", direction="minimize")
"""

"""
study = optuna.create_study(storage="sqlite:///basic_lstm50IPT1.db", study_name="IPTFOR_lstm50-5-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm50IPT1.db", study_name="IPTFOR_lstm50-5-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm50IPT1.db", study_name="IPTFOR_lstm50-5-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///basic_lstm50IPT2.db", study_name="IPTFOR_lstm50-10-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm50IPT2.db", study_name="IPTFOR_lstm50-10-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm50IPT2.db", study_name="IPTFOR_lstm50-10-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///basic_lstm50IPT3.db", study_name="IPTFOR_lstm50-15-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm50IPT3.db", study_name="IPTFOR_lstm50-15-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm50IPT3.db", study_name="IPTFOR_lstm50-15-2", direction="minimize")
"""


"""
study = optuna.create_study(storage="sqlite:///basic_lstm50IPT11.db", study_name="RESFOR_lstm50-5-0", direction="minimize")

study = optuna.create_study(storage="sqlite:///basic_lstm50IPT11.db", study_name="RESFOR_lstm50-5-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm50IPT11.db", study_name="RESFOR_lstm50-5-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///basic_lstm50IPT22.db", study_name="RESFOR_lstm50-10-0", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm50IPT22.db", study_name="RESFOR_lstm50-10-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm50IPT22.db", study_name="RESFOR_lstm50-10-2", direction="minimize")

study = optuna.create_study(storage="sqlite:///basic_lstm50IPT33.db", study_name="RESFOR_lstm50-15-0", direction="minimize")

study = optuna.create_study(storage="sqlite:///basic_lstm50IPT33.db", study_name="RESFOR_lstm50-15-1", direction="minimize")
study = optuna.create_study(storage="sqlite:///basic_lstm50IPT33.db", study_name="RESFOR_lstm50-15-2", direction="minimize")
"""

#study.optimize(objective, n_trials=3)

#loaded_study = optuna.load_study(study_name="my_secstudy", storage="sqlite:///example.db")
#assert len(loaded_study.trials) == len(study.trials)
