from typing import Any, Mapping, Optional, Sequence, Union

PrimitiveData = Optional[Union[str, int, float, bool]]

QueryParams = Mapping[str, Union[PrimitiveData, Sequence[PrimitiveData]]]
Headers = Mapping[str, str]
Cookies = Mapping[str, str]
FormData = Mapping[str, Any]
JsonData = Any
Files = Mapping[str, bytes]
Auth = tuple[str, str]
