Certainly! Below are the specific commands you'll need for setting up your Frappe environment and working with DocTypes. These commands can be added to your GitHub `README.md` file for easy reference.

---

# **Frappe Bench Setup Guide**

## **Introduction**
This guide provides the essential commands to set up a Frappe environment using Docker and to create and manage DocTypes in ERPNext.

## **Installation Commands**

### **Using Docker**

1. **Pull Debian Image**
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

4. **Update and Upgrade Packages**
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

7. **Edit MySQL Configuration**
    ```bash
    nano /etc/mysql/my.cnf
    ```

8. **Restart MySQL Service**
    ```bash
    service mariadb restart
    ```

9. **Install Node Version Manager (NVM)**
    ```bash
    curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
    source ~/.profile
    ```

10. **Install Node.js**
    ```bash
    nvm install 18
    ```

11. **Install Yarn**
    ```bash
    npm install -g yarn
    ```

12. **Install Frappe Bench**
    ```bash
    pip3 install frappe-bench
    ```

13. **Initialize Frappe Bench**
    ```bash
    bench init --frappe-branch version-15 frappe-bench
    cd frappe-bench
    ```

14. **Change Permissions**
    ```bash
    chmod -R o+rx /home/[frappe-user]
    ```

15. **Create a New Site**
    ```bash
    bench new-site [site-name]
    ```

16. **Install ERPNext App**
    ```bash
    bench get-app --branch version-15 erpnext
    bench --site [site-name] install-app erpnext
    ```

17. **Start Bench**
    ```bash
    bench start
    ```

## **Creating DocTypes**

### **Student DocType**

1. **Create Student DocType**
    ```bash
    bench --site [site-name] new-doctype Student
    ```

2. **Navigate to DocType**
    ```bash
    bench --site [site-name] migrate
    ```

### **Program DocType**

1. **Create Program DocType**
    ```bash
    bench --site [site-name] new-doctype Program
    ```

2. **Navigate to DocType**
    ```bash
    bench --site [site-name] migrate
    ```

### **Course DocType**

1. **Create Course DocType**
    ```bash
    bench --site [site-name] new-doctype Course
    ```

2. **Navigate to DocType**
    ```bash
    bench --site [site-name] migrate
    ```

### **Topic DocType**

1. **Create Topic DocType**
    ```bash
    bench --site [site-name] new-doctype Topic
    ```

2. **Navigate to DocType**
    ```bash
    bench --site [site-name] migrate
    ```

## **Custom API Commands**

### **Create Custom API File**

1. **Navigate to Custom App Directory**
    ```bash
    cd /home/[frappe-user]/frappe-bench/apps/[custom_app]/[custom_app]/api
    ```

2. **Create Python File for API**
    ```bash
    touch student_api.py
    ```

3. **Edit File**
    ```bash
    nano student_api.py
    ```

4. **Migrate Changes**
    ```bash
    bench --site [site-name] migrate
    ```

## **Role Permissions and Restrictions**

### **Set Role Permissions**

1. **Go to Role Permissions Manager**
    ```bash
    bench --site [site-name] open-ui
    ```

2. **Assign Permissions**
    ```bash
    # In the UI, navigate to Role Permissions Manager and set permissions for roles.
    ```

---

### **References**
- [Frappe Installation Guide](https://wiki.nestorbird.com/wiki/install-frappe-v15)
- [GitHub Repository](https://github.com/D-codE-Hub/Frappe-ERPNext-Version-15--in-Ubuntu-22.04-LTS)
- [Code with Karani](https://codewithkarani.com/2023/12/31/how-to-install-erpnext-version-15-in-ubuntu-a-step-by-step-guide/)

---

These commands will guide you through the installation and initial setup of Frappe, as well as the creation and management of custom DocTypes and APIs.
