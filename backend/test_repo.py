from app.repositories.material_repository import MaterialRepositoryStub

repo = MaterialRepositoryStub()
profiles = repo.get_all_profiles()
print(f'Репозиторий работает. Найдено профилей: {len(profiles)}')
print(f'Первый профиль: {profiles[0].name if profiles else "Нет данных"}')

# Дополнительная проверка
profile = repo.get_profile('I-beam_20B1')
if profile:
    print(f'Профиль I-beam_20B1 найден: {profile.name}')
    print(f'Момент инерции: {profile.moment_of_inertia_ix_cm4} см⁴')
else:
    print('Профиль I-beam_20B1 не найден')
    