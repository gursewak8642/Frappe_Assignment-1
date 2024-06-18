Here's a comprehensive guide on how to set up and work with Frappe, including creating DocTypes, custom fields, and configuring CRUD operations. This guide also covers installation steps and Docker commands to set up your Frappe environment. The guide is divided into several parts to make it easier to follow and understand.

---

## **Frappe Introduction Guide**

### **Objective**
- To understand the Frappe framework structure.
- To learn how to create and customize DocTypes, child DocTypes, file structures.
- To perform CRUD operations and apply various customizations.

---

### **1. Setting Up Frappe Environment**

#### **Using Docker**

1. **Pull Debian Image from Docker Hub**
   ```bash
   docker pull debian:10
   ```

2. **Create a New Container**
   ```bash
   docker run -dt --name bench_v13 -p 8788:8000 debian:10 /bin/bash
   ```

3. **Access the Container**
   ```bash
   docker exec -it bench_v13 /bin/bash
   ```

4. **Set Up Environment**
   ```bash
   apt-get update -y
   apt-get upgrade -y
   ```

5. **Install Required Packages**
   ```bash
   apt-get install git python3-dev python3.10-dev python3-setuptools python3-pip python3-distutils python3.10-venv mariadb-server mariadb-client redis-server xvfb libfontconfig wkhtmltopdf libmysqlclient-dev curl npm -y
   ```

6. **Secure MySQL Installation**
   ```bash
   mysql_secure_installation
   ```

7. **MySQL Configuration**
   ```bash
   nano /etc/mysql/my.cnf
   ```
   Add the following block:
   ```ini
   [mysqld]
   character-set-client-handshake = FALSE
   character-set-server = utf8mb4
   collation-server = utf8mb4_unicode_ci

   [mysql]
   default-character-set = utf8mb4
   ```
   Restart MySQL:
   ```bash
   service mariadb restart
   ```

8. **Install Node Version Manager (NVM)**
   ```bash
   curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
   source ~/.profile
   nvm install 18
   ```

9. **Install Yarn**
   ```bash
   npm install -g yarn
   ```

10. **Install Frappe Bench**
    ```bash
    pip3 install frappe-bench
    ```

11. **Initialize Frappe Bench**
    ```bash
    bench init --frappe-branch version-15 frappe-bench
    cd frappe-bench
    chmod -R o+rx /home/[frappe-user]
    ```

12. **Create a New Frappe Site**
    ```bash
    bench new-site [site-name]
    ```

13. **Install ERPNext App**
    ```bash
    bench get-app --branch version-15 erpnext
    bench --site [site-name] install-app erpnext
    ```

14. **Start Bench**
    ```bash
    bench start
    ```

---

### **2. Creating DocTypes**

#### **DocType: Student**

1. **Create the DocType**
   ```bash
   bench --site [site-name] new-doctype Student
   ```

2. **Add Fields in `Student` DocType:**
    - **First Name**
    - **Middle Name**
    - **Last Name**
    - **Full Name** (Read-only, concatenated)
    - **Naming Series** (e.g., STU-YYYY-MM-DATE-0001)
    - **Create User** (Button)
    - **Student Email Address** (with validations)
    - **Date of Birth** (with validations)
    - **Gender**
    - **Nationality**
    - **Blood Group** (Select)
    - **Default Address** (Link to CRM Module)
    - **HTML Field** (Shows combined address)
    - **Joining Date** (Prefilled with today's date)
    - **Active** (Checkbox)

3. **Script to Concatenate Full Name:**
    ```python
    frappe.ui.form.on('Student', {
        first_name: function(frm) {
            frm.set_value('full_name', `${frm.doc.first_name} ${frm.doc.middle_name} ${frm.doc.last_name}`);
        },
        middle_name: function(frm) {
            frm.set_value('full_name', `${frm.doc.first_name} ${frm.doc.middle_name} ${frm.doc.last_name}`);
        },
        last_name: function(frm) {
            frm.set_value('full_name', `${frm.doc.first_name} ${frm.doc.middle_name} ${frm.doc.last_name}`);
        },
        create_user: function(frm) {
            frappe.call({
                method: "create_student_user",
                args: { email: frm.doc.student_email_address },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint("User created successfully.");
                    }
                }
            });
        }
    });
    ```

4. **Validate Email:**
    ```python
    frappe.ui.form.on('Student', {
        validate: function(frm) {
            if (!frm.doc.student_email_address.includes('@')) {
                frappe.throw("Invalid email address");
            }
        }
    });
    ```

5. **Create User Button Script:**
    ```python
    @frappe.whitelist()
    def create_student_user(email):
        if not frappe.db.exists("User", {"email": email}):
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": "Student",
                "roles": [{"role": "Student"}]
            })
            user.insert()
            return True
        return False
    ```

#### **DocType: Program**

1. **Create the DocType**
   ```bash
   bench --site [site-name] new-doctype Program
   ```

2. **Add Fields in `Program` DocType:**
    - **Program Name** (Data)
    - **Description** (Text)
    - **Start Date** (Date)
    - **End Date** (Date)
    - **Duration** (Float)
    - **Total Credits** (Float, Sum of course credits)
    - **Status** (Select: Planned, Ongoing, Completed)
    - **Instructor** (Link to Employee, filter by Instructor role)
    - **Participants** (Child Table with Participant and Preview button)
    - **Courses** (Child Table with Course link)

3. **Script for Preview Button:**
    ```python
    frappe.ui.form.on('Program Participant', {
        preview: function(frm, cdt, cdn) {
            const row = locals[cdt][cdn];
            frappe.call({
                method: "get_student_picture",
                args: { student: row.participant },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(`<img src="${response.message}" width="100">`);
                    }
                }
            });
        }
    });
    ```

4. **Server Script for Preview:**
    ```python
    @frappe.whitelist()
    def get_student_picture(student):
        user = frappe.db.get_value("Student", student, "user_id")
        if user:
            return frappe.db.get_value("User", user, "user_image")
        return None
    ```

#### **DocType: Course**

1. **Create the DocType**
   ```bash
   bench --site [site-name] new-doctype Course
   ```

2. **Add Fields in `Course` DocType:**
    - **Course Name** (Data)
    - **Course Code** (Data)
    - **Credits** (Float)
    - **Academic Year** (Link)
    - **Topics** (Child Table with `Topic` link)

#### **DocType: Topic**

1. **Create the DocType**
   ```bash
   bench --site [site-name] new-doctype Topic
   ```

2. **Add Fields in `Topic` DocType:**
    - **Topic Name** (Data)
    - **Topic Description** (Text)

---

### **3. Custom CRUD APIs**

1. **Create Custom API Endpoint:**
   Create a file `student_api.py` under `frappe-bench/apps/[custom_app]/[custom_app]/api`.

2. **Sample CRUD Operations:**
    ```python
    @frappe.whitelist(allow_guest=True)
    def create_student(data):
        student = frappe.new_doc("Student")
        student.update(data)
        student.insert()
        return student

    @frappe.whitelist(allow_guest=True)
    def read_student(student_name):
        return frappe.get_doc("Student", student_name)

    @frappe.whitelist(allow_guest=True)
    def update_student(data):
        student = frappe.get_doc("Student", data['name'])
        student.update(data)
        student.save()
        return student

    @frappe.whitelist(allow_guest=True)
    def delete_student(student_name):
        frappe.delete_doc("Student", student_name)
        return "Student deleted"
    ```

3. **Validation Example:**
    ```python
    def validate_student_data(data):
        if not 'student_email_address' in data or not '@' in data['student_email_address']:
            frappe.throw("Invalid email address.")
    ```

---

### **4. Role Permissions and Restrictions**

1. **Set Permissions in `Student` and `Instructor` Roles:**
    - Go to `Role Permissions Manager` in ERPNext.
    - Select `Student` and `Instructor` roles.
    - Assign

 `Read`, `Write`, `Create`, and `Delete` permissions to relevant DocTypes.

2. **Restrict Access to Fields:**
    - Use `Custom Script` to restrict visibility of fields based on roles.
    ```python
    frappe.ui.form.on('Student', {
        refresh: function(frm) {
            if (frappe.user.has_role('Student')) {
                frm.set_df_property('fieldname', 'read_only', 1);
            }
        }
    });
    ```

---

### **5. README for GitHub**

Create a `README.md` file with the following content:

---

# **Frappe Bench Setup Guide**

## **Introduction**
This guide will help you set up a Frappe environment using Docker and provides steps to create and customize DocTypes in ERPNext.

## **Installation**

### **Using Docker**

1. **Pull Docker Image:**
    ```bash
    docker pull debian:10
    ```

2. **Run Docker Container:**
    ```bash
    docker run -dt --name bench_v13 -p 8788:8000 debian:10 /bin/bash
    ```

3. **Access Container:**
    ```bash
    docker exec -it bench_v13 /bin/bash
    ```

4. **Update and Install Packages:**
    ```bash
    apt-get update -y
    apt-get upgrade -y
    apt-get install git python3-dev python3.10-dev python3-setuptools python3-pip python3-distutils python3.10-venv mariadb-server mariadb-client redis-server xvfb libfontconfig wkhtmltopdf libmysqlclient-dev curl npm -y
    ```

5. **Secure MySQL Installation:**
    ```bash
    mysql_secure_installation
    ```

6. **Configure MySQL:**
    ```bash
    nano /etc/mysql/my.cnf
    ```
    Add:
    ```ini
    [mysqld]
    character-set-client-handshake = FALSE
    character-set-server = utf8mb4
    collation-server = utf8mb4_unicode_ci

    [mysql]
    default-character-set = utf8mb4
    ```
    Restart:
    ```bash
    service mariadb restart
    ```

7. **Install Node Version Manager:**
    ```bash
    curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
    source ~/.profile
    nvm install 18
    ```

8. **Install Yarn:**
    ```bash
    npm install -g yarn
    ```

9. **Install Frappe Bench:**
    ```bash
    pip3 install frappe-bench
    ```

10. **Initialize Frappe Bench:**
    ```bash
    bench init --frappe-branch version-15 frappe-bench
    cd frappe-bench
    chmod -R o+rx /home/[frappe-user]
    ```

11. **Create a New Site:**
    ```bash
    bench new-site [site-name]
    ```

12. **Install ERPNext App:**
    ```bash
    bench get-app --branch version-15 erpnext
    bench --site [site-name] install-app erpnext
    ```

13. **Start Bench:**
    ```bash
    bench start
    ```

## **Creating DocTypes**

### **Student DocType**

1. **Create Student DocType:**
    ```bash
    bench --site [site-name] new-doctype Student
    ```

2. **Add Fields and Custom Scripts.**

### **Program DocType**

1. **Create Program DocType:**
    ```bash
    bench --site [site-name] new-doctype Program
    ```

2. **Add Fields and Custom Scripts.**

## **Custom API Endpoints**

1. **Create API File:**
    ```bash
    [path/to/custom_app]/api/student_api.py
    ```

2. **Add CRUD Operations.**

## **Role Permissions**

1. **Set Role Permissions in ERPNext.**

---

This README file can be added to your GitHub repository to provide a step-by-step setup guide for the Frappe environment.

### **References**
- [Frappe Installation Guide](https://wiki.nestorbird.com/wiki/install-frappe-v15)
- [GitHub Repository](https://github.com/D-codE-Hub/Frappe-ERPNext-Version-15--in-Ubuntu-22.04-LTS)
- [Code with Karani](https://codewithkarani.com/2023/12/31/how-to-install-erpnext-version-15-in-ubuntu-a-step-by-step-guide/)

---

This guide should help you get started with Frappe, from setting up your environment to creating and customizing your DocTypes.
