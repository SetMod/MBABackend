
def test_new_role(db, roles):
    user_role = roles(role_name='User',
                      role_description='Roles for standard user')
    db.session.add(user_role)
    db.session.commit()

    assert user_role.role_id == 1
    assert user_role.role_name == 'User'
    assert user_role.role_description == 'Roles for standard user'


def test_get_all_roles(db, roles):
    all_roles = db.session.query(roles).all()

    assert isinstance(all_roles, list)


def test_get_role_by_name(db, roles):
    role = db.session.query(roles).where(roles.role_name == 'User').first()

    assert isinstance(role, roles)
    assert role.role_id == 1
    assert role.role_name == 'User'
    assert role.role_description == 'Roles for standard user'


def test_role_schema_dum(db, roles, roles_schema):
    role = db.session.query(roles).where(roles.role_name == 'User').first()
    dump_role = roles_schema.dump(role)

    assert isinstance(dump_role, dict)
    assert dump_role['role_id'] == 1
    assert dump_role['role_name'] == 'User'
    assert dump_role['role_description'] == 'Roles for standard user'


def test_role_schema_dump_many(db, roles, roles_schema):
    all_roles = db.session.query(roles).all()
    dump_role = roles_schema.dump(all_roles, many=True)

    assert isinstance(dump_role, list)
    assert isinstance(dump_role[0], dict)

# def test_new_user():
#     user = Users(user_first_name='Testfirstname',
#                  user_second_name='Testsecondname',
#                  user_email='test@test.com',
#                  user_phone='+01234567890',
#                  user_username='testuser',
#                  user_password='testpass',
#                  role_id=1)
#     assert user.user_first_name == 'Testfirstname'
#     assert user.user_second_name == 'Testsecondname'
#     assert user.user_email == 'test@test.com'
#     assert user.user_phone == '+01234567890'
#     assert user.user_username == 'testuser'
#     assert user.user_password == 'testpass'
#     assert user.role_id == 1
