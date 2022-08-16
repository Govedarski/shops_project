def assert_count_equal(count, model):
    assert len(model.query.all()) == count
