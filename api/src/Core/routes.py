from src.Core.general.general import index
from src.Core.general.general import clear
from src.Core.general.general import update
from src.Core.general.general import find
from src.Core.user.accounts import login
from src.Core.user.accounts import signup
from src.Core.user.accounts import compeleteSignUp
from src.Core.user.accounts import getUserInfo
from src.Core.user.books import newBook
from src.Core.user.books import updateBook
from src.Core.user.books import getBookInfo
from src.Core.user.books import insertComment
def dispacther():

    dispatch={
        "index":index,
        "clear":clear,
        "update":update,
        "find":find,
        "login":login,
        "login-userinfo":getUserInfo,
        
        "signup":signup,
        "signup-compelete":compeleteSignUp,
        "books-newbook":newBook,
        "books-updatebook":updateBook,
        "books-info":getBookInfo,
        "books-comment":insertComment
    }
    return dispatch