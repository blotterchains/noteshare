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
from src.Core.user.accounts import cashout as ucashout
from src.Core.user.books import newBook
from src.Core.user.books import updateBook
from src.Core.user.books import getBookInfo
from src.Core.user.books import insertComment
from src.Core.admin.admin import deleteBook
from src.Core.admin.admin import allcashout
from src.Core.admin.admin import payCashout
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
        "login-cashout":ucashout,
        ###############################signup routes
        "signup":signup,
        "signup-compelete":compeleteSignUp,
        ###############################books routes
        "books-newbook":newBook,
        "books-updatebook":updateBook,
        "books-info":getBookInfo,
        "books-comment":insertComment,
        ###############################admin routes
        "admin-deleteBook":deleteBook,
        "admin-paycashout":payCashout,
        "admin-allcashout":allcashout
    }
    return dispatch