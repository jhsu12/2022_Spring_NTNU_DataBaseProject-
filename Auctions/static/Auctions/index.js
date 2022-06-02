function sort_category(s)
{
  const searchParams1 = new URLSearchParams(window.location.search);
  const hostname = window.location.hostname;
  console.log(searchParams1);
  //console.log(s.id);
  
  let sort_url = `?category=${s.id}`
  if(searchParams1.has('time'))
  {
    sort_url = sort_url + `&&time=${searchParams1.get('time')}`
  }
  window.location.href = sort_url;
  console.log(searchParams1.get('c'));
  console.log(sort_url);
  
}

function sort_time(t)
{
  console.log(t);
  const searchParams1 = new URLSearchParams(window.location.search);
  let sort_url = `?time=${t}`
  if(searchParams1.has('category'))
  {
    sort_url = sort_url + `&&category=${searchParams1.get('category')}`
  }
  window.location.href = sort_url;
}