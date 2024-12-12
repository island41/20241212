from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# 資料庫連接函數
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 主頁路由
@app.route('/')
def index():
    return render_template('view_customers.html')

# 新增客戶頁面路由
@app.route('/add_customer')
def add_customer():
    return render_template('add_customer.html')

# 編輯客戶頁面路由
@app.route('/edit_customer/<int:id>')
def edit_customer(id):
    return render_template('edit_customer.html')

# API 端點：獲取所有客戶資料
@app.route('/api/customers')
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM customers ORDER BY id DESC')
    customers = cursor.fetchall()
    
    customers_list = []
    for customer in customers:
        customer_dict = dict(customer)
        customer_dict['created_at'] = datetime.strptime(
            customer_dict['created_at'], '%Y-%m-%d %H:%M:%S'
        ).strftime('%Y-%m-%d %H:%M:%S')
        customers_list.append(customer_dict)
    
    conn.close()
    return jsonify(customers_list)

# API 端點：新增客戶
@app.route('/api/customers', methods=['POST'])
def create_customer():
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO customers (name, contact_info, company_name, notes, phone, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['contact_info'],
            data['company_name'],
            data['notes'],
            data['phone'],
            data['email']
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': '客戶資料新增成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# API 端點：獲取單個客戶資料
@app.route('/api/customers/<int:id>', methods=['GET'])
def get_customer(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM customers WHERE id = ?', (id,))
        customer = cursor.fetchone()
        
        if customer is None:
            return jsonify({'success': False, 'message': '找不到客戶資料'})
        
        customer_dict = dict(customer)
        customer_dict['created_at'] = datetime.strptime(
            customer_dict['created_at'], '%Y-%m-%d %H:%M:%S'
        ).strftime('%Y-%m-%d %H:%M:%S')
        
        conn.close()
        return jsonify({'success': True, 'customer': customer_dict})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# API 端點：更新客戶資料
@app.route('/api/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE customers 
            SET name = ?, contact_info = ?, company_name = ?, 
                notes = ?, phone = ?, email = ?
            WHERE id = ?
        ''', (
            data['name'],
            data['contact_info'],
            data['company_name'],
            data['notes'],
            data['phone'],
            data['email'],
            id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': '客戶資料更新成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# API 端點：刪除客戶
@app.route('/api/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM customers WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': '客戶資料已刪除'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
