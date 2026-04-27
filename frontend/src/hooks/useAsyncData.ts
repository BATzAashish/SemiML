import { useEffect, useState } from "react";

export function useAsyncData(loader) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    setLoading(true);
    loader()
      .then((result) => active && setData(result))
      .catch((err) => active && setError(err?.message || "Unable to load data"))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [loader]);

  return { data, loading, error };
}
