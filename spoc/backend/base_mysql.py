import pymysql

""" 
# 索引index
# 1. 
# CREATE UNIQUE INDEX index01 
# ON TABLE column;
# 2. 
"""

"""
# 触发器trigger

"""

"""
# 存储过程

"""


class MySQL:

    def getCourseInfo(self, courseId):
        connection, cursor = self.connectDatabase()
        result = ""
        instruction = "SELECT ans.id, ans.n, teacher.name, ans.mid, ans.mn, ans.i, ans.degree " \
                      "FROM " \
                      " (SELECT c.id, c.introduction, c.name, cm.material_id, cm.name, c.degree " \
                      "FROM course as c LEFT OUTER JOIN (select * from material, course_material where course_material.material_id=material.id) AS cm " \
                      "ON (c.id=cm.course_id) ) AS ans(id, i, n,mid, mn, degree), teacher_course AS tc, teacher " \
                      "WHERE tc.course_id=ans.id AND tc.teacher_id=teacher.id AND ans.id=%s"

        cursor.execute(instruction, [courseId])
        result = cursor.fetchall()
        self.closeDatabase(connection, cursor)
        return result

    def GetCourseDegree(self, id):
        result = self.getCourseDegree(id)
        # 返回课程对应的评价表，计算平均值交给前端
        # 评价表为{1：float， 2：float， 3：float， 4：float， 5：float, totalNum: number, avgDegree(平均分): float}
        # print(result)
        dic = {"1": result[0][1], "2": result[0][2], "3": result[0][3],
               "4": result[0][4], "5": result[0][5], "totalNum": result[0][6],
               "avgDegree": result[0][7]}
        print(dic)

    def getPostTheme(self, postthemeId):
        connection, cursor = self.connectDatabase()
        result = ""
        try:
            instruction = "SELECT id, title, content, `time`, isTeacher FROM posttheme " \
                          "where id=%s"
            cursor.execute(instruction, [postthemeId])
            result = cursor.fetchall()
            type = result[0][4]
            # print(type)
            if type == 0:
                instruction = "SELECT id, `name` FROM student, student_posttheme as sp where " \
                              "sp.student_id=student.id and sp.posttheme_id=%s"
            elif type == 1:
                instruction = "SELECT id, `name` FROM teacher, teacher_posttheme as tp where " \
                              "tp.teacher_id=teacher.id and tp.posttheme_id=%s"
            else:
                instruction = "SELECT id, `name` FROM `admin`, admin_posttheme as ap where " \
                              "ap.admin_id=`admin`.id and ap.posttheme_id=%s"
            cursor.execute(instruction, [postthemeId])
            result += cursor.fetchall()
            # print(result)
        except Exception as e:
            connection.rollback()
            print("error")
        self.closeDatabase(connection, cursor)
        return result

    def getCourseDegree(self, courseID):
        connection, cursor = self.connectDatabase()
        result = ""
        try:
            cursor.callproc('COMMENT_DEGREE', args=(courseID, 0, 0, 0, 0, 0, 0, 0))
            cursor.execute(query='select @_COMMENT_DEGREE_0, @_COMMENT_DEGREE_1,@_COMMENT_DEGREE_2,@_COMMENT_DEGREE_3,'
                                 '@_COMMENT_DEGREE_4,@_COMMENT_DEGREE_5,@_COMMENT_DEGREE_6, @_COMMENT_DEGREE_7;')
            result = cursor.fetchall()
        except Exception as e:
            connection.rollback()
            print("error")
        self.closeDatabase(connection, cursor)
        return result

    def getTeacherDisCussNum(self, userName):
        connection, cursor = self.connectDatabase()
        instruction = "SELECT count_discuss FROM teacher where id=%s"
        result = ""
        try:
            cursor.execute(instruction, [userName])
            result = cursor.fetchall()
        except Exception as e:
            connection.rollback()
            print("error")
        self.closeDatabase(connection, cursor)
        return result

    def getTeacherCourseNum(self, userName):
        connection, cursor = self.connectDatabase()
        instruction = "SELECT count_course FROM teacher where id=%s"
        result = ""
        try:
            cursor.execute(instruction, [userName])
            result = cursor.fetchall()
        except Exception as e:
            connection.rollback()
            print("error")
        self.closeDatabase(connection, cursor)
        return result

    def getStudentDiscussNum(self, userName):
        connection, cursor = self.connectDatabase()
        instruction = "SELECT count_discuss FROM student where id=%s"
        result = ""
        try:
            cursor.execute(instruction, [userName])
            result = cursor.fetchall()
        except Exception as e:
            connection.rollback()
            print("error")
        self.closeDatabase(connection, cursor)
        return result

    def getStudentCommentNum(self, userName):
        connection, cursor = self.connectDatabase()
        instruction = "SELECT count_comment FROM student where id=%s"
        result = ""
        try:
            cursor.execute(instruction, [userName])
            result = cursor.fetchall()
        except Exception as e:
            connection.rollback()
            print("error")
        self.closeDatabase(connection, cursor)
        return result

    def getStudentCourseNum(self, userName):
        connection, cursor = self.connectDatabase()
        instruction = "SELECT count_course FROM student where id=%s"
        result = ""
        try:
            cursor.execute(instruction, [userName])
            result = cursor.fetchall()
        except Exception as e:
            connection.rollback()
            print("error")
        self.closeDatabase(connection, cursor)
        return result

    def procedure01(self):
        connection, cursor = self.connectDatabase()

        cursor.callproc()
        self.closeDatabase(connection, cursor)
        return

    def adminChange(self, username, password):
        connection, cursor = self.connectDatabase()

        instruction = "UPDATE `admin` " \
                      "SET password=%s " \
                      "WHERE id=%s"
        try:
            cursor.execute(instruction, [password, username])
            connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def getTeacherList(self):
        connection, cursor = self.connectDatabase()
        instruction = "SELECT id, name from teacher"
        try:
            cursor.execute(instruction)
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        result = cursor.fetchall()
        self.closeDatabase(connection, cursor)
        return result

    def getStudentList(self):
        connection, cursor = self.connectDatabase()

        instruction = "SELECT id,name FROM student"
        try:
            cursor.execute(instruction)
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        result = cursor.fetchall()
        self.closeDatabase(connection, cursor)
        return result

    def findAdmin(self, admin_id):
        connection, cursor = self.connectDatabase()

        instruction = "SELECT *\
                FROM admin\
                Where id=%s"
        try:
            cursor.execute(instruction, [admin_id])
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        result = cursor.fetchall()
        self.closeDatabase(connection, cursor)
        return result

    def deletePostTheme(self, postThemeId):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "DELETE FROM post " \
                          "WHERE id in (" \
                          "SELECT post_id from post_posttheme where posttheme_id=%s" \
                          ")"
            cursor.execute(instruction, [postThemeId])
            connection.commit()
            instruction = "DELETE FROM posttheme " \
                          "WHERE id=%s"
            cursor.execute(instruction, [postThemeId])
            connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def deleteComment(self, commentId):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "DELETE FROM comment " \
                          "where id=%s"
            cursor.execute(instruction, [commentId])
            connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def deletePost(self, postId):
        connection, cursor = self.connectDatabase()
        try:
            # 这里只需要删除post，关系设置了外键，自动删除消失的post的关系
            instruction = "DELETE FROM post " \
                          "WHERE id=%s"
            cursor.execute(instruction, [postId])
            connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def getPostList(self, postThemeId):
        connection, cursor = self.connectDatabase()
        result = ""
        try:
            instruction = "SELECT p.id, s.id, s.name, p.content, p.time, p.isTeacher FROM " \
                          "post as p, student_post as sp, student as s, post_posttheme as pp " \
                          "WHERE pp.posttheme_id=%s and pp.post_id=p.id and p.id=sp.post_id and sp.student_id=s.id "
            # "ORDER by p.time desc"
            cursor.execute(instruction, [postThemeId])
            result = cursor.fetchall()

            instruction = "SELECT p.id, t.id, t.name, p.content, p.time, p.isTeacher FROM " \
                          "post as p, teacher_post as tp, teacher as t, post_posttheme as pp " \
                          "WHERE pp.posttheme_id=%s and pp.post_id=p.id and p.id=tp.post_id and tp.teacher_id=t.id "
            # "ORDER by p.time desc"
            cursor.execute(instruction, [postThemeId])
            result += cursor.fetchall()

            instruction = "SELECT p.id, t.id, t.name, p.content, p.time, p.isTeacher FROM " \
                          "post as p, admin_post as tp, `admin` as t, post_posttheme as pp " \
                          "WHERE pp.posttheme_id=%s and pp.post_id=p.id and p.id=tp.post_id and tp.admin_id=t.id "
            # "ORDER by p.time desc"
            cursor.execute(instruction, [postThemeId])
            result += cursor.fetchall()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return result

    def buildPost(self, postThemeId, userName, content, ti, isTeacher):
        connection, cursor = self.connectDatabase()
        try:
            cursor.callproc("BUILDP", args=(postThemeId, userName, content, ti, isTeacher))
            # instruction = "INSERT INTO post( content, time, isTeacher) " \
            #               "values(%s, %s, %s)"
            # cursor.execute(instruction, [content, ti, isTeacher])
            # connection.commit()
            #
            # instruction = "SELECT MAX(id) FROM post"
            #
            # cursor.execute(instruction)
            # result = cursor.fetchall();
            # result = result[0][0]
            #
            # if isTeacher == 0 or isTeacher == "0":
            #     instruction = "INSERT INTO student_post(student_id, post_id) " \
            #                   "VALUES (%s, %s)"
            # elif isTeacher == 2 or isTeacher == "2":
            #     instruction = "INSERT INTO admin_post(admin_id, post_id) " \
            #                   "VALUES (%s, %s)"
            # else:
            #     instruction = "INSERT INTO teacher_post(teacher_id, post_id) " \
            #                   "VALUES (%s, %s)"
            # cursor.execute(instruction, [userName, result])
            #
            # connection.commit()
            #
            # instruction = "INSERT INTO post_posttheme(posttheme_id, post_id) " \
            #               "VALUES (%s, %s)"
            # cursor.execute(instruction, [postThemeId, result])
            #
            # connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def getPostThemeList(self):
        connection, cursor = self.connectDatabase()
        result = ""
        try:
            instruction = "SELECT s.id, s.name, pt.title, pt.content, pt.time, pt.id, pt.isTeacher FROM " \
                          "posttheme as pt, student_posttheme as sp, student as s " \
                          "WHERE pt.id=sp.posttheme_id AND sp.student_id=s.id "
            # "ORDER BY pt.id"
            cursor.execute(instruction)
            result = cursor.fetchall()

            instruction = "SELECT t.id, t.name, pt.title, pt.content, pt.time, pt.id, pt.isTeacher FROM " \
                          "posttheme as pt, teacher_posttheme as tp, teacher as t " \
                          "WHERE pt.id=tp.posttheme_id AND tp.teacher_id=t.id "
            # "ORDER BY pt.id"
            cursor.execute(instruction)
            result += cursor.fetchall()

            instruction = "SELECT t.id, t.name, pt.title, pt.content, pt.time, pt.id, pt.isTeacher FROM " \
                          "posttheme as pt, admin_posttheme as tp, `admin` as t " \
                          "WHERE pt.id=tp.posttheme_id AND tp.admin_id=t.id "
            # "ORDER BY pt.id"
            cursor.execute(instruction)
            result += cursor.fetchall()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return result

    def buildPostTheme(self, userName, title, content, ti, isTeacher):
        connection, cursor = self.connectDatabase()
        try:
            cursor.callproc('BUILDPT', args=(userName, title, content, ti, isTeacher))
            # instruction = "INSERT INTO posttheme(title, content, time, isTeacher) " \
            #               "values(%s, %s, %s, %s)"
            # cursor.execute(instruction, [title, content, ti, isTeacher])
            # connection.commit()
            #
            # instruction = "SELECT MAX(id) FROM posttheme"
            #
            # cursor.execute(instruction)
            # result = cursor.fetchall();
            # result = result[0][0]
            #
            # if isTeacher == 0 or isTeacher == "0":
            #     instruction = "INSERT INTO student_posttheme(student_id, posttheme_id) " \
            #                   "VALUES (%s, %s)"
            # elif isTeacher == 2 or isTeacher == "2":
            #     instruction = "INSERT INTO admin_posttheme(admin_id, posttheme_id) " \
            #                   "VALUES (%s, %s)"
            # else:
            #     instruction = "INSERT INTO teacher_posttheme(teacher_id, posttheme_id) " \
            #                   "VALUES (%s, %s)"
            # cursor.execute(instruction, [userName, result])
            #
            # connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def getCommentList(self, courseId):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "SELECT s.id, s.name, cc.c, cc.time, cc.id, cc.d FROM " \
                          "(SELECT `time`, content, id, `degree` FROM comment, course_comment as cc " \
                          "WHERE cc.course_id=%s and cc.comment_id=comment.id) AS cc(time,c,id,d), " \
                          "student_comment as sc, student AS s " \
                          "WHERE cc.id=sc.comment_id AND sc.student_id=s.id "
            # "ORDER BY cc.time desc"

            cursor.execute(instruction, [courseId])
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        result = cursor.fetchall()
        self.closeDatabase(connection, cursor)
        return result

    def commentCourse(self, courseId, userName, content, ti, degree):
        connection, cursor = self.connectDatabase()
        if degree == "None":
            degree = 5
        try:
            cursor.callproc("COMMENT", args=(courseId, userName, content, ti, degree))
            # instruction = "INSERT INTO comment(content, time) " \
            #               "values(%s, %s)"
            #
            # cursor.execute(instruction, [content, ti])
            #
            # connection.commit()
            #
            # instruction = "SELECT MAX(id) FROM comment"
            #
            # cursor.execute(instruction)
            # result = cursor.fetchall()
            # result = result[0][0]
            #
            # instruction = "INSERT INTO student_comment(student_id, comment_id) " \
            #               "VALUES (%s, %s)"
            #
            # cursor.execute(instruction, [userName, result])
            #
            # connection.commit()
            #
            # instruction = "INSERT INTO course_comment(course_id, comment_id, degree) " \
            #               "VALUES (%s, %s, %s)"
            #
            # cursor.execute(instruction, [courseId, result, degree])
            #
            # connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def getMaterialName(self, material_id):
        connection, cursor = self.connectDatabase()

        instruction = "SELECT name " \
                      "FROM material " \
                      "WHERE id=%s"
        cursor.execute(instruction, [material_id])

        result = cursor.fetchall()

        self.closeDatabase(connection, cursor)
        return result

    def deleteMaterial(self, teached_id, material_id):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "DELETE FROM material " \
                          "WHERE id=%s"

            cursor.execute(instruction, [material_id])
            connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def getTeacherMaterialList(self, teacher_id):
        connection, cursor = self.connectDatabase()

        instruction = "SELECT m.id, m.name " \
                      "FROM material AS m, teacher_material AS tm " \
                      "WHERE tm.teacher_id=%s AND tm.material_id=m.id"

        cursor.execute(instruction, [teacher_id])

        result = cursor.fetchall()
        self.closeDatabase(connection, cursor)
        return result

    def getMaterialList(self):
        connection, cursor = self.connectDatabase()

        instruction = "SELECT id, name " \
                      "FROM material "

        cursor.execute(instruction)

        result = cursor.fetchall()
        self.closeDatabase(connection, cursor)
        return result

    def buildMaterial(self, teacher_id, materialName):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "INSERT INTO material(name) " \
                          "VALUES(%s) "

            cursor.execute(instruction, [materialName])
            connection.commit()

            instruction = "SELECT id " \
                          "FROM material " \
                          "WHERE name=%s"

            cursor.execute(instruction, [materialName])
            result = cursor.fetchall()

            material_id = result[len(result) - 1][0]

            instruction = "INSERT INTO teacher_material(teacher_id, material_id) " \
                          "VALUES(%s, %s)"
            cursor.execute(instruction, [teacher_id, material_id])
            connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def connectDatabase(self):
        connection = pymysql.connect(host="rm-2zeu3f7e1n5yt10v0co.mysql.rds.aliyuncs.com",
                                     db="spoc",
                                     user="root",
                                     passwd="myja&*$4X579cKr",
                                     charset="utf8")
        cursor = connection.cursor()
        return connection, cursor

    def findStudentCourse(self, student_id, course_id):
        connection, cursor = self.connectDatabase()

        instruction = "SELECT *\
                    FROM student_course\
                    Where student_id=%s AND course_id=%s"
        cursor.execute(instruction, [student_id, course_id])
        result = cursor.fetchall()
        self.closeDatabase(connection, cursor)
        return result

    def selectCourse(self, student_id, course_id):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "INSERT INTO student_course(student_id, course_id) " \
                          "values(%s, %s)"
            cursor.execute(instruction, [student_id, course_id])
            connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def dropStudentCourse(self, student_id, course_id):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "DELETE FROM student_course " \
                          "WHERE student_id=%s AND course_id=%s "
            cursor.execute(instruction, [student_id, course_id])
            connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def getTeacherCourseList(self, teacher_id):
        connection, cursor = self.connectDatabase()

        instruction = "SELECT ans.id, ans.n, teacher.name, ans.mid, ans.mn, ans.i " \
                      "FROM " \
                      " (SELECT c.id, c.introduction, c.name, cm.material_id, cm.name " \
                      "FROM course as c LEFT OUTER JOIN (select * from material, course_material where course_material.material_id=material.id) AS cm " \
                      "ON (c.id=cm.course_id) ) AS ans(id, i, n,mid, mn), teacher_course AS tc, teacher " \
                      "WHERE tc.course_id=ans.id AND tc.teacher_id=teacher.id AND teacher.id=%s "
        # "ORDER BY ans.id"

        cursor.execute(instruction, [teacher_id])
        return cursor.fetchall()

        self.closeDatabase(connection, cursor)

        return result

    def getStudentCourseList(self, student_id):
        connection, cursor = self.connectDatabase()

        instruction = "SELECT ans.id, ans.n, teacher.name, ans.mid, ans.mn, ans.i " \
                      "FROM " \
                      " (SELECT c.id, c.introduction, c.name, cm.material_id, cm.name " \
                      "FROM course as c LEFT OUTER JOIN (select * from material, course_material where course_material.material_id=material.id) AS cm " \
                      "ON (c.id=cm.course_id) ) AS ans(id, i, n,mid, mn), teacher_course AS tc, teacher, student_course as sc " \
                      "WHERE tc.course_id=ans.id AND tc.teacher_id=teacher.id AND ans.id=sc.course_id AND sc.student_id=%s "
        # "ORDER BY ans.id"

        cursor.execute(instruction, [student_id])

        result = cursor.fetchall()
        self.closeDatabase(connection, cursor)
        return result

    def getCourseList(self):
        connection, cursor = self.connectDatabase()

        instruction = "SELECT ans.id, ans.n, teacher.name, ans.mid, ans.mn, ans.i, ans.degree " \
                      "FROM " \
                      " (SELECT c.id, c.introduction, c.name, cm.material_id, cm.name, c.degree " \
                      "FROM course as c LEFT OUTER JOIN (select * from material, course_material where course_material.material_id=material.id) AS cm " \
                      "ON (c.id=cm.course_id) ) AS ans(id, i, n,mid, mn, degree), teacher_course AS tc, teacher " \
                      "WHERE tc.course_id=ans.id AND tc.teacher_id=teacher.id "
        # "ORDER BY ans.id"

        cursor.execute(instruction)
        result = cursor.fetchall()
        self.closeDatabase(connection, cursor)
        return result

    def buildCourseMaterial(self, course_id, material_id):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "INSERT INTO course_material(material_id, course_id) " \
                          "VALUES(%s, %s)"
            cursor.execute(instruction, [material_id, course_id])
            connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def buildCourse(self, teacher_id, course_name, materialIdList, introduction):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "INSERT INTO course(name, introduction) " \
                          "VALUES(%s, %s)"
            cursor.execute(instruction, [course_name, introduction])
            connection.commit()

            instruction = "SELECT max(id) " \
                          "FROM course "
            cursor.execute(instruction)
            result = cursor.fetchall()

            course_id = result[0][0]

            instruction = "INSERT INTO teacher_course(teacher_id, course_id) " \
                          "VALUES(%s, %s)"

            cursor.execute(instruction, [teacher_id, course_id])
            connection.commit()

            if (materialIdList[0] != ''):

                for material_id in materialIdList:
                    if material_id == "":
                        continue

                    self.buildCourseMaterial(course_id, material_id)

            self.closeDatabase(connection, cursor)
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        return

    def closeDatabase(self, connection, cursor):
        connection.close()
        cursor.close()

    def registerStudent(self, student_id, password, student_name):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "INSERT INTO student(id, password, name) " \
                          "values(%s, %s, %s)"

            cursor.execute(instruction, [student_id, password, student_name])
            connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def registerTeacher(self, teacher_id, password, teacher_name):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "INSERT INTO teacher(id, password, name) " \
                          "values(%s, %s, %s)"

            cursor.execute(instruction, [teacher_id, password, teacher_name])
            connection.commit()
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        self.closeDatabase(connection, cursor)
        return

    def findTeacher(self, teacher_id):
        connection, cursor = self.connectDatabase()

        instruction = "SELECT *\
                FROM teacher\
                Where id=%s"

        cursor.execute(instruction, [teacher_id])

        result = cursor.fetchall()

        self.closeDatabase(connection, cursor)

        return result

    def findStudent(self, student_id):
        connection, cursor = self.connectDatabase()

        instruction = "SELECT *\
                FROM student\
                Where id=%s"

        cursor.execute(instruction, [student_id])

        result = cursor.fetchall()

        self.closeDatabase(connection, cursor)

        return result

    def studentPasswordChange(self, student_id, password):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "UPDATE student " \
                          "SET password=%s " \
                          "WHERE id=%s"
            cursor.execute(instruction, [password, student_id])

            connection.commit()
            self.closeDatabase(connection, cursor)
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        return

    def changeCourse(self, teacher_id, course_id, course_name, materialIdList, introduction):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "UPDATE course " \
                          "SET name=%s, introduction=%s " \
                          "WHERE id=%s"
            cursor.execute(instruction, [course_name, introduction, course_id])
            connection.commit()

            # 找旧的课程资料id：
            instruction = "SELECT m.id " \
                          "FROM material AS m, course_material AS cm " \
                          "WHERE cm.material_id=m.id AND cm.course_id=%s"
            cursor.execute(instruction, [course_id])
            result = cursor.fetchall()

            print(result)
            print(materialIdList)

            for item in result:
                material_id = str(item[0])
                if materialIdList.count(material_id):
                    materialIdList.remove(material_id)
                else:
                    instruction = "DELETE FROM course_material " \
                                  "WHERE course_id=%s AND material_id=%s"
                    cursor.execute(instruction, [course_id, material_id])
                    connection.commit()

            for material_id in materialIdList:
                if material_id == "":
                    continue
                self.buildCourseMaterial(course_id, material_id)

            self.closeDatabase(connection, cursor)
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        return

    def cancelCourse(self, teacher_id, course_id):
        connection, cursor = self.connectDatabase()

        # 不要删除课程对应的材料
        # instruction = "DELETE FROM material AS m " \
        #               "WHERE id IN " \
        #               "(" \
        #               "SELECT material_id " \
        #               "FROM course_material AS cm " \
        #               "WHERE cm.course_id=%s" \
        #               ")"
        # cursor.execute(instruction, [course_id])
        # connection.commit()
        print(course_id)


        instruction = "SELECT comment_id from course_comment WHERE course_id=%s"
        cursor.execute(instruction, [course_id])
        result = cursor.fetchall()
        print(result)
        for i in result:
            instruction = "DELETE FROM comment " \
                      "WHERE id=%s"
            cursor.execute(instruction, [i[0]])
        print(1)

        instruction = "SELECT student_id from student_course where course_id=%s"
        cursor.execute(instruction, [course_id])
        result = cursor.fetchall()
        print(result)
        for i in result:
            instruction = "UPDATE student set count_course = count_course - 1" \
                          " where id=%s"
            cursor.execute(instruction, [i[0]])

        instruction = "DELETE FROM course " \
                      "WHERE id=%s"
        cursor.execute(instruction, [course_id])
        connection.commit()
        self.closeDatabase(connection, cursor)
        return

    def teacherPasswordChange(self, teacher_id, password):
        connection, cursor = self.connectDatabase()
        try:
            instruction = "UPDATE teacher " \
                          "SET password=%s " \
                          "WHERE id=%s"
            cursor.execute(instruction, [password, teacher_id])

            connection.commit()
            self.closeDatabase(connection, cursor)
        except Exception as e:
            connection.rollback()
            print("执行MySQL错误")
        return

    def test(self):
        connection, cursor = self.connectDatabase()

        instruction = "SELECT MAX(id) FROM course "

        cursor.execute(instruction)

        result = cursor.fetchall()
        print(type(result[0][0]))

        self.closeDatabase(connection, cursor)
        return


if __name__ == "__main__":
    sql = MySQL()
    result = sql.getCourseInfo(109)
    CourseList = []
    for item in result:
        CourseList.append({'id': item[0], 'name': item[1], 'teacherName': item[2], 'introduction': item[5] if
        item[5] is not None else '', 'materialList': [], 'm_id': item[3] if item[3] is not None else '',
                           'm_name': item[4] if item[4] is not None else ''})
    i = 0
    while i < len(CourseList):
        if CourseList[i]['m_id'] != '' and len(CourseList[i]['materialList']) == 0:
            CourseList[i]['materialList'].append(
                {'id': CourseList[i]['m_id'], 'name': CourseList[i]['m_name']});

        if i != len(CourseList) - 1 and CourseList[i]['id'] == CourseList[i + 1]['id']:
            CourseList[i]['materialList'].append(
                {'id': CourseList[i + 1]['m_id'], 'name': CourseList[i + 1]['m_name']});
            CourseList.pop(i + 1)
            i -= 1
        i += 1
    print(CourseList[0])
    # r = sql.getPostTheme(42)
    # dic = {"id": r[0][0], "userName": r[1][0], "userNickName": r[1][1],
    #        "title": r[0][1], "content": r[0][2], "time": r[0][3],
    #        "isTeacher": r[0][4]}
    # print(dic)
    # sql.test()
    # result = sql.getStudentCourseNum("19373136")
    # print(result[0][0])
    #
    # sql.getCourseDegree(26)
    #
    # sql.commentCourse(1, 19373136, 1, "2021-20-22 11:12:22")
    #
    # result = sql.getCommentList("1")
    # commentList = []
    #
    # for item in result:
    #     commentList.append({"userName": item[0],
    #                         "userNickName": item[1],
    #                         "content": item[2],
    #                         "time": item[3]})
    #
    # print(commentList)
    # sql = MySQL()
    # # sql.buildMaterial("123", "234")
    # result = sql.getMaterialList()
    # print(result)
    #
    # result = sql.getTeacherMaterialList("123")
    # print(result)
    """
    userName = "19373136"
    sql = MySQL()
    sql.dropStudentCourse(userName, "5")
    # select_course(userName, "2")
    result = sql.getStudentCourseList(userName)
    print(result)

    result = sql.findStudentCourse(userName, "4")
    flag = not not result
    print(flag)
    sql.teacherPasswordChange("123", "123456")
    # sql.create_course("13","线性代数2")
    """

    """
    create table
    create_student = "CREATE TABLE `student` (`username` varchar(20) NOT NULL PRIMARY KEY, " \
                     "`password` varchar(32) NOT NULL);"
    
    try:
        cursor.execute(create_student)
    except Exception as e:
        print("exception occured: ", e)
    """
