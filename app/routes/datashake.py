from flask import Blueprint, render_template, request, redirect, url_for
from app.database.db_source import db, Employee
from app.database.db_target import Summary
from sqlalchemy import update, not_, func, select
from app.database import db_source, db_target
from decimal import Decimal

datashake_bp = Blueprint('datashake', __name__)

@datashake_bp.route('/docs')
def datashakeDocs():
    return render_template('datashakeDocs.html')

@datashake_bp.route("/datashake", methods=["GET", "POST"])
def datashake_index():
    if request.method == "POST":
        # Obtener datos del formulario
        name = request.form.get('name-form')
        department = request.form.get('department-user')
        salary = request.form.get('salary-form')
        hours = request.form.get('hours-form')

        # Crear y guardar nuevo empleado
        new_employee = Employee(name=name, department=department, salary=salary, hours=hours)
        db.session.add(new_employee)
        print(f"Datos recibidos: {name}, {department}, {salary}")

        db.session.commit()
        print("Empleado guardado correctamente")
        
        return redirect(url_for('datashake.datashake_index'))

    employee_item = Employee.query.all()
    summary_item = Summary.query.all()
    source_column_names = [column.name for column in Employee.__table__.columns]
    target_column_names = [column.name for column in Summary.__table__.columns]

    return render_template("datashake.html", employees=employee_item, summaries=summary_item, source_column_names=source_column_names, target_column_names=target_column_names)

@datashake_bp.route("/data_transformation", methods=['GET', 'POST'])
def data_transformation():
    if request.method == "POST":
        db_selection = request.form.get('db-selection')
        source_column = request.form.get('origin-selection')
        target_column = request.form.get('target-selection')
        text_transformation = request.form.get('data-text-transformation')
        concat_text = request.form.get('concat-text', '').strip()
        replace_text = request.form.get('text-to-replace', '').strip()
        with_text = request.form.get('replace-with', '').strip()
        number_transformation = request.form.get('data-num-transformation')
        value_number_transformation = request.form.get('number-input-transformation')
        target_transformation_selection = request.form.get('target-selection')
        

        # Imprimir valores recibidos para depuración
        print(f"db: {db_selection}")
        print(f"source_column: {source_column}")
        print(f"target_column: {target_column}")
        print(f"text_transformation: {text_transformation}")
        print(f"concat_text: {concat_text}")
        print(f"replace_text: {replace_text}")
        print(f"with_text: {with_text}")
        print(f"Number transformation: {number_transformation}")
        #print(type(getattr(Employee, source_column).type))
        print(f'Target selection: {target_transformation_selection}')



        if db_selection == 'source-database':

            if text_transformation == 'concatenate':
                # Actualización masiva para Concatenar
                stmt = (
                    update(Employee)
                    .values({source_column: getattr(Employee, source_column) + concat_text})
                )
                print(f"Ejecutando actualización de concatenación para la columna {source_column} con el texto: {concat_text}")
                print(f"Actualización realizada para la columna {source_column} con el texto concatenado.")

            elif text_transformation == 'replace':
                # Actualización masiva para Reemplazar
                stmt = (
                    update(Employee)
                    .values({source_column: func.replace(getattr(Employee, source_column), replace_text, with_text)})
                )
                print(f"Reemplazando '{replace_text}' con '{with_text}'")

            elif text_transformation == 'lower':
                # Convertir a minúsculas
                stmt = (
                    update(Employee).values({source_column: func.lower(getattr(Employee, source_column))})
                )
                print("Convierte a minúsculas")

            elif text_transformation == 'upper':
                # Convertir a mayúsculas
                stmt = (
                    update(Employee).values({source_column: func.upper(getattr(Employee, source_column))})
                )
                print("Convierte a mayúsculas")

            # Construye el statement según la operación
            if number_transformation == 'sum':
                value_number_transformation = Decimal(str(value_number_transformation))
                stmt = update(Employee).values({
                    source_column: getattr(Employee, source_column) + value_number_transformation
                })
                print(f"Se sumó {value_number_transformation} a cada fila de {source_column}")

            elif number_transformation == 'min':
                value_number_transformation = Decimal(str(value_number_transformation))
                stmt = update(Employee).values({
                    source_column: getattr(Employee, source_column) - value_number_transformation
                })
                print(f"Se restó {value_number_transformation} a cada fila de {source_column}")

            elif number_transformation == 'multiply':
                value_number_transformation = Decimal(str(value_number_transformation))
                stmt = update(Employee).values({
                    source_column: getattr(Employee, source_column) * value_number_transformation
                })
                print(f"Se multiplicó cada fila de {source_column} por {value_number_transformation}")

            elif number_transformation == 'div':
                value_number_transformation = Decimal(str(value_number_transformation))
                if value_number_transformation == 0:
                    raise ValueError("No se puede dividir por cero.")
                stmt = update(Employee).values({
                    source_column: getattr(Employee, source_column) / value_number_transformation
                })
                print(f"Se dividió cada fila de {source_column} entre {value_number_transformation}")

            # Ejecuta y redirige si se construyó un statement
            if 'stmt' in locals():
                db.session.execute(stmt)
                db.session.commit()

            return redirect(url_for('datashake.datashake_index'))
        
        else:
            if target_transformation_selection == 'employee-count':
                # Contar empleados agrupados por departamento, en minúscula
                counts = db.session.query(
                    func.lower(Employee.department).label('department'),
                    func.count(Employee.id).label('count')
                ).group_by(func.lower(Employee.department)).all()

                # Recorrer los resultados y actualizar la tabla Summary
                for dept_lower, count in counts:
                    # Buscar coincidencia insensible a mayúsculas
                    summary = Summary.query.filter(func.lower(Summary.department) == dept_lower).first()
                    
                    if summary:
                        summary.employee_count = count
                    else:
                        # (Opcional) crear nuevo registro si no existe
                        summary = Summary(department=dept_lower, employee_count=count)
                        db.session.add(summary)

                db.session.commit()

            elif target_transformation_selection == 'avg-salary':
                # Calcular promedio de salario por departamento en minúsculas
                averages = db.session.query(
                    func.lower(Employee.department).label('department'),
                    func.avg(Employee.salary).label('avg_salary')
                ).group_by(func.lower(Employee.department)).all()

                for dept_lower, avg_salary in averages:
                    summary = Summary.query.filter(func.lower(Summary.department) == dept_lower).first()
                    
                    if summary:
                        summary.salary_sum = avg_salary
                    else:
                        # (Opcional) crear si no existe
                        summary = Summary(department=dept_lower, salary_sum=avg_salary)
                        db.session.add(summary)

                db.session.commit()

            elif target_transformation_selection == 'avg-hours':

                hours_averages = db.session.query(
                    func.lower(Employee.department).label('department'),
                    func.avg(Employee.hours).label('hours')
                ).group_by(func.lower(Employee.department)).all()

                for dept_lower, avg_hours in hours_averages:
                    summary = Summary.query.filter(func.lower(Summary.department) == dept_lower).first()

                    if summary:
                        summary.hours_sum = avg_hours
                    else:
                        # (Opcional) crear si no existe
                        summary = Summary(department=dept_lower, hours_sum=hours_averages)
                        db.session.add(summary)

                db.session.commit()

            
            return redirect(url_for('datashake.datashake_index'))



    employee_item = Employee.query.all()
    summary_item = Summary.query.all()
    source_column_names = [column.name for column in Employee.__table__.columns]
    target_column_names = [column.name for column in Summary.__table__.columns]

    return render_template("datashake.html", employees=employee_item, summaries=summary_item, source_column_names=source_column_names, target_column_names=target_column_names)
