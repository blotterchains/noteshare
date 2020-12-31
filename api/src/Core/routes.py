from src.Core.general.general import index
from src.Core.general.general import clear
from src.Core.general.general import update
from src.Core.general.general import find
from src.Core.user.accounts import login
from src.Core.user.accounts import signup
from src.Core.user.accounts import compeleteSignUp
from src.Core.user.accounts import getUserInfo
from src.Core.user.accounts import buyNewBook
from src.Core.user.accounts import updateOrdersBook
from src.Core.user.books import newBook
from src.Core.user.books import updateBook
from src.Core.user.books import getBookInfo
from src.Core.user.books import insertComment
def dispacther():

    dispatch={
        ###############################general routes
        "index":index,
        "clear":clear,
        "update":update,
        "find":find,
        ###############################accounts routes
        "login":login,
        "login-userinfo":getUserInfo,
        "login-order":buyNewBook,
        "login-updateorder":updateOrdersBook,
        ###############################signup routes
        "signup":signup,
        "signup-compelete":compeleteSignUp,
        ###############################books routes
        "books-newbook":newBook,
        "books-updatebook":updateBook,
        "books-info":getBookInfo,
        "books-comment":insertComment
    }
    return dispatch