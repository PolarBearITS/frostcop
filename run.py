import importlib
monitors = ['supreme']

def run_mon(mon):
	mon.run()

threads = []
for name in monitors:
	s = name.split('-')
	if len(s) == 1:
		m = getattr(importlib.import_module('monitors'), name)()
	else:
		m = getattr(importlib.import_module(f'monitors.{s[0]}'), s[1])()
	run_mon(m)