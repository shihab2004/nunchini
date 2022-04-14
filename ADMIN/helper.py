from Product.models import Order
def order_yearly_chart_report(year,status):
     return {
            "jan":Order.objects.filter(ordered_time__year=year,ordered_time__month=1,order_status=status).count(),
            "feb":Order.objects.filter(ordered_time__year=year,ordered_time__month=2,order_status=status).count(),
            "mar":Order.objects.filter(ordered_time__year=year,ordered_time__month=3,order_status=status).count(),
            "apr":Order.objects.filter(ordered_time__year=year,ordered_time__month=4,order_status=status).count(),
            "may":Order.objects.filter(ordered_time__year=year,ordered_time__month=5,order_status=status).count(),
            "jun":Order.objects.filter(ordered_time__year=year,ordered_time__month=6,order_status=status).count(),
            "jul":Order.objects.filter(ordered_time__year=year,ordered_time__month=7,order_status=status).count(),
            "aug":Order.objects.filter(ordered_time__year=year,ordered_time__month=8,order_status=status).count(),
            "sep":Order.objects.filter(ordered_time__year=year,ordered_time__month=9,order_status=status).count(),
            "oct":Order.objects.filter(ordered_time__year=year,ordered_time__month=10,order_status=status).count(),
            "nov":Order.objects.filter(ordered_time__year=year,ordered_time__month=11,order_status=status).count(),
            "dec":Order.objects.filter(ordered_time__year=year,ordered_time__month=12,order_status=status).count(),
        }
    
from datetime import datetime
def sealize_time(date_sting):
    y_m_d = date_sting.split("T")[0]
    h_m = date_sting.split("T")[1]
    
    y_m_d_sss = y_m_d.split("-")
    h_m_sss = h_m.split(":")
    
    
    return datetime(int(y_m_d_sss[0]),int(y_m_d_sss[1]),int(y_m_d_sss[2]),int(h_m_sss[0]),int(h_m_sss[1]))