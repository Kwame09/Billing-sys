#!python
# -*- coding: utf-8 -*-
# @Date    : 2022-07-29 15:28:22
# @Author  : Amos Amissah (theonlyamos@gmail.com)
# @Link    : link
# @Version : 1.0.0


class SessionManager(dict):
    '''
    Class for managing sessions
    '''

    def __setitem__(self, key, item) -> None:
        self.__dict__[key] = item
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __repr__(self) -> str:
        return repr(self.__dict__)
    
    def __len__(self) -> int:
        return len(self.__dict__)
    
    def __delitem__(self, key) -> None:
        del self.__dict__[key]
    
    def clear(self) -> None:
        return self.__dict__.clear()
    
    def copy(self):
        return self.__dict__.copy()
    
    def has_key(self, key):
        return key in self.__dict__
    
    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)
    
    def keys(self) -> list:
        return self.__dict__.keys()
    
    def values(self) -> list:
        return self.__dict__.values()
    
    def items(self):
        return self.__dict__.items()
    
    def pop(self, *args):
        return self.__dict__.pop(*args)
    
    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)
    
    def __contains__(self, item) -> bool:
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

