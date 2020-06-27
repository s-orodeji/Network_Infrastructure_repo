from nornir.plugins.tasks.data import load_yaml
from nornir.plugins.tasks.text import template_file
from nornir.plugins.tasks.networking import napalm_configure

path = "./nornir_config/values"
def configure_rip(task):
    data = task.run(
                     task=load_yaml,
              file=f'{path}/{task.host}.yaml'
       )
    task.host["interface"] = data.result["interface"]
    r_rip = task.run(task=template_file,
                    template="rip.j2", path="./nornir_config/templates/", interface= data.result["interface"])
    task.host["template_config"] = r_rip.result
    task.run(task=napalm_configure, configuration=task.host["template_config"])