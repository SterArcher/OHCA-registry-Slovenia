use std::{collections::HashMap, hash::Hash};

pub struct QueryResult<T: Hash + Eq> {
    pub value: T,
    pub count: i64,
}

impl<T: Hash + Eq> QueryResult<T> {
    fn new(value: T, count: i64) -> Self {
        Self { value, count }
    }
}

pub trait ToQueryResultHashMap<T: Hash + Eq> {
    fn to_hashmap(self) -> HashMap<T, i64>;
}

impl ToQueryResultHashMap<Option<i16>> for Vec<QueryResult<Option<i16>>> {
    fn to_hashmap(self) -> HashMap<Option<i16>, i64> {
        let mut hashmap = HashMap::new();

        for res in self {
            hashmap.insert(res.value, res.count);
        }

        hashmap
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vec_to_hashmap() {
        let vec = vec![
            QueryResult::new(Some(-1), 10),
            QueryResult::new(Some(0), 20),
            QueryResult::new(Some(1), 5),
            QueryResult::new(None, 12),
        ];

        let hashmap = HashMap::from([(Some(-1), 10), (Some(0), 20), (Some(1), 5), (None, 12)]);

        assert_eq!(vec_to_hashmap(vec), hashmap);
    }
}
