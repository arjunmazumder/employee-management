import pymysql
# PyMySQL কে Django এর জন্য প্রস্তুত করা
pymysql.version_info = (2, 2, 8, "final", 0) # এখানে ভার্সনটি বাড়িয়ে দিন
pymysql.install_as_MySQLdb()