"""
@file

@brief @see cl Database
"""

import re
import copy
import random
import sqlite3 as SQLite
import datetime
import decimal
import numpy


from .file_text_binary import TextFile
from .database_exception import ExceptionSQL


class NoHeaderException(Exception):

    """
    just to be meant to be caucht later by a unit test
    """
    pass


class DatabaseCore2:

    """
    Complementary methods for class @see cl Database.
    """

    _split_expr = "\\r?\\t"

    def _check_connection(self):
        """
        Checks the SQL connection.
        """
        if "_connection" not in self.__dict__:
            message = "use connect method before doing operation on this database"
            raise Exception(message)

    def _check_values(self, values):
        """
        When values are inserted or updated, this method doubles ``"'"``
        it does not allow str values, only str.

        @param      values      dictionary
        @return                 dictionary
        """
        mod = []
        for k, v in values.items():
            if isinstance(v, str) and "'" in v:
                mod.append(k)
        if len(mod) == 0:
            return values
        else:
            values = copy.copy(values)
            for k in mod:
                values[k] = values[k].replace("'", "''")
            return values

    def summary(self, light=False):
        """
        Returns the list of tables, their columns, and their length.

        @param      light   light version, no count, no first lines
        @return             a dictionary where the keys are (t,i), t is a table name, i is in ["columns", "size", "first_lines"],
                            a str message
        """
        tables = self.get_table_list()
        indexes = self.get_index_list()
        res = {}
        lines = []

        for t in tables:
            col = self.get_table_columns_list(t)
            if not light:
                size = self.get_table_nb_lines(t)
                first = self.get_table_nfirst_lines(t)
            else:
                size = -1
                first = []

            res[t, "columns"] = col
            res[t, "size"] = size
            res[t, "first_lines"] = first

            lines.append(t + "\t" + str(size) + " records")
            lines.append("    columns")
            for c in col:
                lines.append("        " + str(c))

            if len(first) > 0:
                lines.append("    first_lines")
                for lf in first:
                    fo = []
                    if lf is None:
                        lines.append("        None")
                    else:
                        for x in lf:
                            if not isinstance(x, str):
                                fo.append(str(x))
                            else:
                                fo.append(x)
                        lines.append("        " + "\t".join(fo))

        if len(indexes) > 0:
            lines.append("\n")
            lines.append("indexes")
            for tu in indexes:
                if isinstance(tu, (tuple, list)):
                    lines.append("    " + "\t".join([str(x) for x in tu]))
                else:
                    lines.append("    " + tu)

        attached = self.get_attached_database_list()
        if len(attached) > 0:
            lines.append("\n")
            lines.append("attached databases")
            for a in attached:
                if a == "main":
                    continue
                lines.append("    " + "\t" + a)
                continue
                # ~ rrr = self.execute(
                #       ~ "SELECT name FROM %s.sqlite_master ORDER BY name;" %
                #       ~ (a,))
                # ~ for b in rrr:
                #       ~ lines.append("       " + "\t" + b[0])

        return res, "\n".join(lines)

    def _guess_columns(
            self, file, format, columns_name=None, filter_case=None, header=True, encoding="utf-8"):
        """
        Guesses the columns types from a file (the method assumes there is a header),
        The types are chosen in that order: int, float, str.
        It keeps the most frequent one with if there is not too many errors.
        The separator must be tabs (``\\t``).

        @param      file            file name
        @param      format          format (only tsv)
        @param      columns_name    if None, the first line contains the columns, otherwise it is the columns name
        @param      filter_case     process every case information (used to replace space for example)
        @param      header          by default, the function is expected a header
        @param      encoding        encoding
        @return                     columns, changes
        """
        f = TextFile(file, fLOG=self.LOG, encoding=encoding)
        f.open()

        if header:
            _aa, _bb, _cc, _dd = f.guess_columns(fields=columns_name)
            reg_exp = re.compile(DatabaseCore2._split_expr.replace(
                "\\t", _cc.replace("|", "[|]")))
        else:
            # tabulation by default
            reg_exp = re.compile(DatabaseCore2._split_expr)
            f.close()
            raise NoHeaderException("a header is expected for that function")

        self.LOG("  [_guess_columns] sep={0}".format([_cc]))

        lines = []
        for line in f:
            if len(lines) > 1000:
                break
            if len(lines) > 900 and random.randint(0, 10) > 0:
                continue
            lines.append(reg_exp.split(
                line.strip(" \r\n").strip('\ufeff')))
        f.close()

        if len(lines) <= 1:
            raise Exception("file %s is empty" % file)

        exp = re.compile("\\W+")
        columns = {}
        done = {}
        count = {}
        changes = {}

        for i in range(0, len(lines[0])):
            if lines[0][i] in [
                    '\ufeffID', '\ufeffid', '\ufeffqid', '\ufeffQID']:
                lines[0][i] = "qid"

            if columns_name is None:
                name = lines[0][i].replace(":", "_")
                origin = lines[0][i]
            else:
                name = columns_name[i].replace(":", "_")
                origin = columns_name[i]

            name = name.replace("-", "_").replace(" ", "_")

            spl = exp.split(name)
            if len(spl) > 1:
                name = "".join(spl)
            if name[0] in "0123456789":
                name = "_" + name

            if name in count:
                count[name] += 1
                name += str(count[name])
            else:
                count[name] = 1

            #lines [0][i] = name
            columns[i] = (name, int)
            done[i] = False

            if origin != name:
                changes[origin] = name

        self.LOG("  [_guess_columns] columns_name={0}".format(columns_name))

        length = {}
        nbline = 0
        count_types = {}

        for line_ in lines[1:]:
            if filter_case is None:
                line = line_
            else:
                line = [filter_case(s) for s in line_]
            nbline += 1
            if line == [] or line == ['']:
                continue

            for i in range(0, len(line)):

                if i >= len(done):
                    # it is probably a wrong line
                    continue

                vl = length.get(i, 0)
                if len(line[i]) > vl:
                    length[i] = len(line[i])

                try:
                    if done[i]:
                        continue
                except KeyError as e:
                    str_columns = ""
                    for k, v in columns.items():
                        str_columns += "       " + \
                            str(k) + "\t" + str(v) + "\n"
                    mes = "KeyError:" + str(e) + "\n" + str(done) + "\n" + str_columns + "\nnb line " + str(
                        nbline) + " columns: " + str(len(line)) + "\n" + str(line)
                    raise RuntimeError(  # pylint: disable=W0707
                        "problem\n" +
                        mes +
                        "\n\ncount_types:\n  " +
                        "\n  ".join(
                            "{0}:{1}".format(
                                k,
                                v) for k,
                            v in sorted(
                                count_types.items())))

                if line[i] is None or len(line[i]) == 0:
                    continue

                try:
                    x = int(line[i])
                    if abs(x) >= 2147483647:
                        raise ValueError("too big int")

                    if i not in count_types:
                        count_types[i] = {int: 1}
                    else:
                        count_types[i][int] = count_types[i].get(int, 0) + 1

                except ValueError:
                    try:
                        x = float(line[i])

                        if i not in count_types:
                            count_types[i] = {float: 1}
                        else:
                            count_types[i][float] = count_types[
                                i].get(float, 0) + 1

                        if columns[i][1] != float:
                            columns[i] = (columns[i][0], float)

                    except ValueError:
                        columns[i] = (
                            columns[i][0], (str, max(
                                1, len(
                                    line[i])) * 2))

                        if i not in count_types:
                            count_types[i] = {str: 1}
                        else:
                            count_types[i][str] = count_types[
                                i].get(str, 0) + 1

        self.LOG("   guess with ", len(lines), "lines")
        self.LOG("   count_types ", count_types)
        for i in range(0, len(columns)):

            # if i is not in count_types, it means the first rows do now
            # contain values for these columns (only null values)
            t = count_types.get(i, {str: 1})
            nb = sum(t.values())

            th = 0.0 if nb < 50 else (
                0.01 if nb < 100 else 0.02)  # we authorize 2% of wrong types

            n = t.get(int, 0)
            if n * 1.0 / nb >= 1 - th:
                ty = int
            else:
                n += t.get(float, 0)
                if n * 1.0 / nb >= 1 - th:
                    ty = float
                else:
                    ty = str

            columns[i] = (columns[i][0], ty)

        self.LOG("   columns ", columns)

        # if not done, choose str by default
        for c in columns:
            v = columns[c]
            if v[1] == str:
                columns[c] = (v[0], (str, max(1, length.get(c, 4)) * 2))

        for c, v in columns.items():
            t = v[1]
            if isinstance(t, tuple) and t[0] == str and t[1] == 0:
                raise Exception(
                    "the length is null for column %s - %s" %
                    (c, str(v)))

        self.LOG("   guess", columns)
        return columns, changes

    def _process_text_line(self, line, columns, format, lower_case, num_line,
                           fill_missing=0, filter_case=None,
                           strict_separator=False):
        """
        Processes a text line.

        @param      line                text line to process (or a list if it already splitted)
        @param      columns             columns definition @see me _append_table
        @param      format              only tsv for the moment
        @param      lower_case          put every str object in lower_case
        @param      num_line            line number
        @param      fill_missing        fill the missing values by a default value, at least not more than fill_missing values
        @param      filter_case         process every case information (used to replace space for example)
        @param      strict_separator    strict number of columns, it assumes there is no separator in the content of every column
        @return                         a dictionary
        """
        if not isinstance(line, list) and not isinstance(
                line, tuple) and not isinstance(line, numpy.ndarray):
            if format != "tsv":
                raise Exception("unable to process format " + format)
            line = line.strip("\r\n ").replace("\n", " ")
            line = DatabaseCore2._split_expr.split(line)

        if filter_case is not None:
            line = [filter_case(s) for s in line]

        try:
            if fill_missing > 0:
                m = max(columns.keys())
                if m >= len(line):
                    line = copy.copy(line)
                    add = 0
                    while m >= len(line) and add < fill_missing:
                        a, b = columns[len(line)]
                        if b is int:
                            line.append("0")
                        elif b is float:
                            line.append("0.0")
                        elif b is decimal.Decimal:
                            line.append("0")
                        elif b is str:
                            line.append("")
                        else:
                            line.append("")
                        add += 1

            res = {}
            for c, v in columns.items():
                if "AUTOFILL" in v:
                    res[v[0]] = "NULL"
                elif "AUTOINCREMENT" in v:
                    continue
                else:
                    if c >= len(line):
                        self.LOG(
                            "(a)line number ",
                            num_line,
                            "*unable to process a line columns ",
                            c,
                            "#",
                            line,
                            " columns ",
                            columns)
                        return None

                    val = line[c]
                    if len(v) > 2 and v[2].lower() not in [
                            "primarykey", "autofill"]:
                        val = v[2](val)

                    try:
                        if isinstance(v[1], tuple):
                            val = v[1][0](val)
                        elif v[1] is datetime.datetime:
                            if isinstance(val, datetime.datetime):
                                pass
                            elif isinstance(val, str):
                                val = datetime.datetime.parse(val)
                            else:
                                raise TypeError(
                                    "unable to convert %s into datetime" % str(
                                        type(val)))
                        else:
                            val = v[1](val)
                    except ValueError:  # as e :
                        self.LOG(
                            "(b)line number ",
                            num_line,
                            "**unable to process a line columns ",
                            c,
                            "#",
                            v[0],
                            " type ",
                            v[1],
                            " value ",
                            repr(
                                line[c]))
                        return None

                    if isinstance(val, str):
                        val = val.replace("'", "''")
                        if lower_case:
                            val = val.lower()
                    res[v[0]] = val

            return res
        except Exception:
            self.LOG("(c)line number", num_line,
                     "***unable to process a line columns:", line)
            return None

    def _get_insert_request(self, dico,
                            table,
                            exe=False,
                            primarykey=None,
                            cursor=None,
                            skip_exception=False):
        """
        Builds an ``INSERT SQL`` request from a dictionary.

        @param      dico            dictionary
        @param      table           table name
        @param      exe             if True, execute the request, if False, do nothing except returning the request
        @param      primarykey      primary key column, if it exist
        @param      cursor          if None, creates a new one, otherwise use it
        @param      skip_exception  if True, log exception instead of raising one
        @return                     str """
        keys = []
        values = []
        for k, v in dico.items():
            keys.append(k)
            if k != primarykey and isinstance(v, str):
                v = "'" + str(v).replace("'", "''") + "'"
                values.append(v)
            elif isinstance(v, datetime.datetime):
                values.append("'" + str(v) + "'")
            else:
                values.append(str(v))
        keys = ",".join(keys)
        values = ",".join(values)
        sql = "INSERT INTO %s (%s) VALUES (%s);" % (table, keys, values)
        if exe:
            try:
                if cursor is not None:
                    cursor.execute(sql)
                else:
                    self._connection.execute(sql)
            except SQLite.OperationalError as e:
                if skip_exception:
                    self.LOG(
                        "OperationalError: unable to execute a query", e, sql)
                else:
                    raise ExceptionSQL(  # pylint: disable=W0707
                        "OperationalError: unable to execute a query", e, sql)
            except SQLite.IntegrityError as e:
                if skip_exception:
                    self.LOG("IntegrityError: unable to execute a query", e, sql)
                else:
                    raise ExceptionSQL(  # pylint: disable=W0707
                        "IntegrityError: unable to execute a query", e, sql)
        return sql

    def get_python_code(self, varname="db"):
        """
        Returns the python code associated to this database.

        @param      varname     name of the variable
        @return                 2-uple: simp, scode (import part, code part)
        """
        simp = ["from pyensae import Database"]

        code = ["tblname = r'%s'" % self.get_file()]

        more = []
        if self._engine != "SQLite":
            code.append("engine = '%s'" % self._engine)
        if self._user is not None:
            code.append("user = '%s'" % self._user)
        if self._password is not None:
            code.append("password = '%s'" % self._password)
        if self._host is not None:
            code.append("host = '%s'" % self._host)
        more = ", ".join(more)

        code.append(
            "%s      = Database (dbfile = tblname%s)" %
            (varname, more))
        code.append("%s.connect ()" % varname)
        att = self.get_attached_database_list(file=True)
        for alias, file in att:
            if len(file) == 0:
                continue
            code.append(
                "%s.attach_database ('%s','%s')" %
                (varname, file, alias))

        return "\n".join(simp) + "\n", "\n".join(code) + "\n"
