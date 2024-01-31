import os,sys
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(parent,"..","..")))

from Drawlib2.tui import single_selector,multi_selector,multi_selector_dir,drawTable

parent = os.path.dirname(__file__)

from Drawlib2.libs.conUtils import clear
clear()

multi_selector_dir(dirpath=parent, sti=0, selTitle="Select an option:", selSuffix=None, dispWidth="vw", stripAnsi=False, formatting={"item_selected":"\x1b[32m","item_normal":"","selector":""}, prMode="cow")

d = {
    "Header1":["elem1","elem2"],
    "Header2":["elem1","elem2"]
}

#drawTable(d)