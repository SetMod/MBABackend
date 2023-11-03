
def test_new_role(db, roles):
    user_role = roles(name='User',
                      description='Roles for standard user')
    db.session.add(user_role)
    db.session.commit()

    assert user_role.role_id == 1
    assert user_role.name == 'User'
    assert user_role.description == 'Roles for standard user'


def test_get_all_roles(db, roles):
    all_roles = db.session.query(roles).all()

    assert isinstance(all_roles, list)


def test_get_role_by_name(db, roles):
    role = db.session.query(roles).where(roles.name == 'User').first()

    assert isinstance(role, roles)
    assert role.id == 1
    assert role.name == 'User'
    assert role.description == 'Roles for standard user'


def test_role_schema_dum(db, roles, roles_schema):
    role = db.session.query(roles).where(roles.name == 'User').first()
    dump_role = roles_schema.dump(role)

    assert isinstance(dump_role, dict)
    assert dump_role['id'] == 1
    assert dump_role['name'] == 'User'
    assert dump_role['description'] == 'Roles for standard user'


def test_role_schema_dump_many(db, roles, roles_schema):
    all_roles = db.session.query(roles).all()
    dump_role = roles_schema.dump(all_roles, many=True)

    assert isinstance(dump_role, list)
    assert isinstance(dump_role[0], dict)

# def test_new_user():
#     user = Users(first_name='Testfirstname',
#                  second_name='Testsecondname',
#                  email='test@test.com',
#                  phone='+01234567890',
#                  username='testuser',
#                  password='testpass',
#                  role_id=1)
#     assert user.first_name == 'Testfirstname'
#     assert user.second_name == 'Testsecondname'
#     assert user.email == 'test@test.com'
#     assert user.phone == '+01234567890'
#     assert user.username == 'testuser'
#     assert user.password == 'testpass'
#     assert user.role_id == 1
