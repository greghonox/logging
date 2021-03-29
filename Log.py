#from scripts.Padroes import DateTime

from logging.handlers import RotatingFileHandler
from gzip import open as openg
from platform import platform
from time import time
import logging
import os

BRR = '\\' if platform().lower() == 'windows' else '/'


class Log(logging.handlers.RotatingFileHandler):
    def __init__(self, filename=r'log\log.txt', **kws):
        self.check_dir_exist(os.path.dirname(filename))
        backupCount = kws.get('backupCount', 0)
        self.backup_count = backupCount
        self.filename = filename
        logging.handlers.RotatingFileHandler.__init__(self, filename, **kws)

    def doArchive(self, old_log):
        with open(old_log) as log:
             with openg(old_log + '.gz', 'wb') as comp_log:
                 comp_log.writelines(map(lambda x: bytes(x, "utf8"), log.readlines()))
        os.remove(old_log)
 
    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backup_count > 0:
            for i in range(self.backup_count - 1, 0, -1):
                sfn = "%s.%d.gz" % (self.baseFilename, i)
                dfn = "%s.%d.gz" % (self.baseFilename, i + 1)
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)

                    # rename(sfn -> dfn)
                    with openg(sfn, "rb") as s, openg(dfn, "wb") as d:
                        d.writelines(s.readlines())
                    
                    os.remove(sfn)
        
        dfn = self.baseFilename + f".1"
        if os.path.exists(dfn):
            os.remove(dfn)
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
            self.doArchive(dfn)
        if not self.delay:
            self.stream = self._open()

    def check_dir_exist(self, caminho):
        try: 
            if(not os.path.isdir(caminho)): os.makedirs(caminho); print(f'CRIANDO A PASTA {caminho} COM SUCESSO')
        except Exception as erro: print(f'ERRO EM CRIAR A PASTA {erro}')
 
        
def mainlog(msg, tipo=1, arq=os.getcwd()+BRR+'log'+BRR+'log.log', 
         mask_g='%(asctime)s - (%(levelname)-8s): %(message)s',
         mask_d='%d/%m/%Y %H:%M:%S', size_max=50000000, size_rotate=10):
	tipos = {1: 'info', 2: 'warning', 3: 'error', 4: 'critical'}

	tipo = tipo if isinstance(tipo, int) else 1 if tipo else 2 if not tipo else tipo
 
	colors = {4: f"\033[91m{msg}\033[0;0m", 1: f"\033[94m{msg}\033[0;0m", 2: f"\033[93m{msg}\033[0;0m", 3: f"\033[1;35m{msg}\033[0;0m"}
	print(colors[tipo])
  
	f = lambda x: eval(f"logging.{tipos[tipo].upper()}")
	
	logging.basicConfig(
	handlers=[Log(arq, maxBytes=size_max,
					   backupCount=size_rotate)],
	level=f(tipo),
	format= mask_g, datefmt=mask_d)
	log = {x: eval(f"logging.{tipos[x]}") for x in tipos}
	log[tipo](msg)


def calcularTempo(f):
    def method(*args, **kwargs):
        tempoIni = time()
        r = f(*args, **kwargs)
        mainlog(f' TEMPO LEVADO PARA ({f.__name__}) REALIZAR {time() - tempoIni}', None)
        return r
    return method


def log(func):
	def method(*args):
		try:
			argumentos = func(*args)
			log = argumentos[0] if(isinstance(argumentos, tuple)) else argumentos

			try: tipo = argumentos[1]
			except: tipo = True
			
			try: log = argumentos[2]
			except: log = None

			mainlog(msg=log, tipo=tipo)
			return argumentos
		except Exception as erro: return f"ERRO EM GERAR LOG {func} --- {args}"
	return method