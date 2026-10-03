"""Set the editable PBIP DataRoot parameter for this local checkout."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
project=ROOT/'dashboard/OLT_Professional_Project'
parameter=project/'OLT.SemanticModel/definition/expressions.tmdl'
parameter.write_text(f'expression DataRoot = "{(project/"data").as_posix()}/" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]\n',encoding='utf-8')
print('Configured DataRoot. Open the PBIP in Desktop and refresh.')
