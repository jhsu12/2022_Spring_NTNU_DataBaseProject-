window.onload = function()
{
  check_sort_time();
}
function check_sort_time()
{
  const searchParams1 = new URLSearchParams(window.location.search);
  if(searchParams1.has('time'))
  {
    //checked current sort method
    document.getElementById(searchParams1.get('time')).selected = true;
    
  }
}
function sort_category(s)
{
  const searchParams1 = new URLSearchParams(window.location.search);
  const hostname = window.location.hostname;
  console.log(searchParams1);
  let id = s.id.replaceAll(' ', '_');;
  console.log(id);
  
  let sort_url = `?category=${id}`
  if(searchParams1.has('time'))
  {
    sort_url = sort_url + `&time=${searchParams1.get('time')}`
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
    sort_url = sort_url + `&category=${searchParams1.get('category')}`
  }
  window.location.href = sort_url;
}