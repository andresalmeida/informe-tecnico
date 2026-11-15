"""The parent covers the risk analysis; the nested headings identify register and summary."""
import json


def run_checks(example, root, checks, build):
    for kind,parent,title,number in [
        ('registro-riesgos','criterios','Análisis de riesgos del proyecto','2'),
        ('evaluacion-impacto-datos','riesgos','Análisis de riesgos del tratamiento','5')]:
        value=json.loads((example.parent/f'ejemplo-{kind}.json').read_text())
        result,pdf=build('riesgos-jerarquia-'+kind,value)
        parent_entry=next(e for e in result['entries'] if e['id']==parent)
        register=next(e for e in result['entries'] if e['kind']=='section' and e['label'].startswith(number+'.1.'))
        summary=next(e for e in result['entries'] if e['kind']=='section' and e['label'].startswith(number+'.2.'))
        assert parent_entry['label']==number+'. '+title
        assert register['label'].split('. ',1)[1]!=title
        assert summary['label'].split('. ',1)[1]!=title
        assert register['level']==summary['level']==parent_entry['level']+1
        checks.append({'case':'riesgos-jerarquia-'+kind,'pages':result['pages']})
