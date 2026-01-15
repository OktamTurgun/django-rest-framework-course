#!/bin/bash

# ============================================================================
# Django REST API - Deployment Scripts Collection
# ============================================================================
# Bu faylda turli deployment scripts to'plangan
# Har bir script'ni alohida faylga ajratib ishlating
# ============================================================================


# ============================================================================
# 1. FULL DEPLOYMENT SCRIPT
# ============================================================================
# File: deploy.sh
# Usage: ./deploy.sh

deploy_full() {
    echo "========================================="
    echo "Django REST API - Full Deployment"
    echo "========================================="
    
    # Configuration
    PROJECT_DIR="/var/www/library-api"
    REPO_URL="https://github.com/yourusername/library-api.git"
    BRANCH="main"
    
    # Colors
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m' # No Color
    
    # Error handling
    set -e
    trap 'echo -e "${RED}Error: Deployment failed!${NC}"' ERR
    
    echo -e "${YELLOW}Starting deployment...${NC}"
    
    # 1. Update system
    echo -e "${YELLOW}[1/10] Updating system...${NC}"
    sudo apt update && sudo apt upgrade -y
    
    # 2. Install dependencies
    echo -e "${YELLOW}[2/10] Installing dependencies...${NC}"
    sudo apt install -y python3-pip python3-venv postgresql nginx redis-server
    
    # 3. Clone or pull repository
    echo -e "${YELLOW}[3/10] Getting latest code...${NC}"
    if [ -d "$PROJECT_DIR" ]; then
        cd $PROJECT_DIR
        git pull origin $BRANCH
    else
        git clone -b $BRANCH $REPO_URL $PROJECT_DIR
        cd $PROJECT_DIR
    fi
    
    # 4. Setup virtual environment
    echo -e "${YELLOW}[4/10] Setting up virtual environment...${NC}"
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    source venv/bin/activate
    
    # 5. Install Python packages
    echo -e "${YELLOW}[5/10] Installing Python packages...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # 6. Run migrations
    echo -e "${YELLOW}[6/10] Running database migrations...${NC}"
    python manage.py migrate --noinput
    
    # 7. Collect static files
    echo -e "${YELLOW}[7/10] Collecting static files...${NC}"
    python manage.py collectstatic --noinput --clear
    
    # 8. Create necessary directories
    echo -e "${YELLOW}[8/10] Creating directories...${NC}"
    mkdir -p logs
    mkdir -p media
    sudo mkdir -p /var/log/gunicorn
    sudo mkdir -p /var/run/gunicorn
    
    # 9. Set permissions
    echo -e "${YELLOW}[9/10] Setting permissions...${NC}"
    sudo chown -R www-data:www-data $PROJECT_DIR
    sudo chmod -R 755 $PROJECT_DIR
    sudo chown -R www-data:www-data /var/log/gunicorn
    sudo chown -R www-data:www-data /var/run/gunicorn
    
    # 10. Restart services
    echo -e "${YELLOW}[10/10] Restarting services...${NC}"
    sudo systemctl restart gunicorn
    sudo systemctl restart nginx
    
    # Verify deployment
    echo -e "${GREEN}=========================================${NC}"
    echo -e "${GREEN}Deployment completed successfully!${NC}"
    echo -e "${GREEN}=========================================${NC}"
    
    # Show service status
    sudo systemctl status gunicorn --no-pager
    sudo systemctl status nginx --no-pager
    
    deactivate
}


# ============================================================================
# 2. BACKUP SCRIPT
# ============================================================================
# File: backup.sh
# Usage: ./backup.sh

backup_system() {
    echo "========================================="
    echo "System Backup Script"
    echo "========================================="
    
    # Configuration
    BACKUP_DIR="/var/backups/library-api"
    PROJECT_DIR="/var/www/library-api"
    DATE=$(date +%Y%m%d_%H%M%S)
    DB_NAME="library_db"
    DB_USER="library_user"
    
    # Create backup directory
    sudo mkdir -p $BACKUP_DIR
    
    echo "[1/4] Backing up database..."
    sudo -u postgres pg_dump $DB_NAME > $BACKUP_DIR/db_$DATE.sql
    
    echo "[2/4] Backing up media files..."
    tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C $PROJECT_DIR media/
    
    echo "[3/4] Backing up configuration..."
    tar -czf $BACKUP_DIR/config_$DATE.tar.gz -C $PROJECT_DIR .env
    
    echo "[4/4] Cleaning old backups (>7 days)..."
    find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
    find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
    
    echo "========================================="
    echo "Backup completed: $DATE"
    echo "Location: $BACKUP_DIR"
    echo "========================================="
    
    # Show backup files
    ls -lh $BACKUP_DIR/
}


# ============================================================================
# 3. UPDATE SCRIPT
# ============================================================================
# File: update.sh
# Usage: ./update.sh

update_application() {
    echo "========================================="
    echo "Application Update Script"
    echo "========================================="
    
    PROJECT_DIR="/var/www/library-api"
    BRANCH="main"
    
    cd $PROJECT_DIR
    
    # 1. Backup before update
    echo "[1/7] Creating backup..."
    ./scripts/backup.sh
    
    # 2. Pull latest changes
    echo "[2/7] Pulling latest changes..."
    git pull origin $BRANCH
    
    # 3. Activate virtual environment
    echo "[3/7] Activating virtual environment..."
    source venv/bin/activate
    
    # 4. Update dependencies
    echo "[4/7] Updating dependencies..."
    pip install -r requirements.txt --upgrade
    
    # 5. Run migrations
    echo "[5/7] Running migrations..."
    python manage.py migrate --noinput
    
    # 6. Collect static files
    echo "[6/7] Collecting static files..."
    python manage.py collectstatic --noinput
    
    # 7. Restart services
    echo "[7/7] Restarting services..."
    sudo systemctl restart gunicorn
    
    echo "========================================="
    echo "Update completed successfully!"
    echo "========================================="
    
    deactivate
}


# ============================================================================
# 4. ROLLBACK SCRIPT
# ============================================================================
# File: rollback.sh
# Usage: ./rollback.sh <commit-hash>

rollback_deployment() {
    echo "========================================="
    echo "Deployment Rollback Script"
    echo "========================================="
    
    if [ -z "$1" ]; then
        echo "Error: Commit hash required"
        echo "Usage: ./rollback.sh <commit-hash>"
        exit 1
    fi
    
    PROJECT_DIR="/var/www/library-api"
    COMMIT_HASH=$1
    
    cd $PROJECT_DIR
    
    echo "[1/6] Creating safety backup..."
    ./scripts/backup.sh
    
    echo "[2/6] Rolling back code to commit: $COMMIT_HASH"
    git checkout $COMMIT_HASH
    
    echo "[3/6] Activating virtual environment..."
    source venv/bin/activate
    
    echo "[4/6] Installing dependencies..."
    pip install -r requirements.txt
    
    echo "[5/6] Running migrations..."
    python manage.py migrate --noinput
    
    echo "[6/6] Restarting services..."
    sudo systemctl restart gunicorn
    
    echo "========================================="
    echo "Rollback completed!"
    echo "========================================="
    
    deactivate
}


# ============================================================================
# 5. HEALTH CHECK SCRIPT
# ============================================================================
# File: healthcheck.sh
# Usage: ./healthcheck.sh

health_check() {
    echo "========================================="
    echo "System Health Check"
    echo "========================================="
    
    # Colors
    GREEN='\033[0;32m'
    RED='\033[0;31m'
    NC='\033[0m'
    
    # Check Gunicorn
    echo -n "Gunicorn status: "
    if systemctl is-active --quiet gunicorn; then
        echo -e "${GREEN}Running${NC}"
    else
        echo -e "${RED}Stopped${NC}"
    fi
    
    # Check Nginx
    echo -n "Nginx status: "
    if systemctl is-active --quiet nginx; then
        echo -e "${GREEN}Running${NC}"
    else
        echo -e "${RED}Stopped${NC}"
    fi
    
    # Check PostgreSQL
    echo -n "PostgreSQL status: "
    if systemctl is-active --quiet postgresql; then
        echo -e "${GREEN}Running${NC}"
    else
        echo -e "${RED}Stopped${NC}"
    fi
    
    # Check Redis
    echo -n "Redis status: "
    if systemctl is-active --quiet redis; then
        echo -e "${GREEN}Running${NC}"
    else
        echo -e "${RED}Stopped${NC}"
    fi
    
    # Check API endpoint
    echo -n "API endpoint: "
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health/ | grep -q "200"; then
        echo -e "${GREEN}Responding${NC}"
    else
        echo -e "${RED}Not responding${NC}"
    fi
    
    # Disk space
    echo ""
    echo "Disk usage:"
    df -h / | tail -1
    
    # Memory usage
    echo ""
    echo "Memory usage:"
    free -h | grep Mem
    
    # Active connections
    echo ""
    echo "Active Gunicorn workers:"
    ps aux | grep gunicorn | grep -v grep | wc -l
    
    echo "========================================="
}


# ============================================================================
# 6. LOG VIEWER SCRIPT
# ============================================================================
# File: logs.sh
# Usage: ./logs.sh [service]

view_logs() {
    SERVICE=${1:-all}
    
    case $SERVICE in
        gunicorn)
            echo "Gunicorn logs:"
            sudo tail -f /var/log/gunicorn/error.log
            ;;
        nginx)
            echo "Nginx logs:"
            sudo tail -f /var/log/nginx/library-api-error.log
            ;;
        django)
            echo "Django logs:"
            tail -f /var/www/library-api/logs/django.log
            ;;
        access)
            echo "Nginx access logs:"
            sudo tail -f /var/log/nginx/library-api-access.log
            ;;
        all)
            echo "All logs (use Ctrl+C to exit):"
            sudo tail -f /var/log/gunicorn/error.log \
                        /var/log/nginx/library-api-error.log \
                        /var/www/library-api/logs/django.log
            ;;
        *)
            echo "Usage: ./logs.sh [gunicorn|nginx|django|access|all]"
            ;;
    esac
}


# ============================================================================
# 7. DATABASE MANAGEMENT SCRIPT
# ============================================================================
# File: db-manage.sh
# Usage: ./db-manage.sh [backup|restore|reset]

manage_database() {
    ACTION=${1:-help}
    DB_NAME="library_db"
    DB_USER="library_user"
    BACKUP_DIR="/var/backups/library-api"
    
    case $ACTION in
        backup)
            echo "Backing up database..."
            DATE=$(date +%Y%m%d_%H%M%S)
            sudo -u postgres pg_dump $DB_NAME > $BACKUP_DIR/manual_db_$DATE.sql
            echo "Backup saved: $BACKUP_DIR/manual_db_$DATE.sql"
            ;;
        restore)
            if [ -z "$2" ]; then
                echo "Error: Backup file required"
                echo "Usage: ./db-manage.sh restore <backup-file>"
                exit 1
            fi
            echo "Restoring database from $2..."
            sudo -u postgres psql $DB_NAME < $2
            echo "Database restored successfully!"
            ;;
        reset)
            read -p "Are you sure you want to reset the database? (yes/no): " confirm
            if [ "$confirm" = "yes" ]; then
                echo "Resetting database..."
                sudo -u postgres psql << EOF
DROP DATABASE IF EXISTS $DB_NAME;
CREATE DATABASE $DB_NAME;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF
                cd /var/www/library-api
                source venv/bin/activate
                python manage.py migrate
                deactivate
                echo "Database reset complete!"
            else
                echo "Reset cancelled"
            fi
            ;;
        *)
            echo "Database Management Script"
            echo "Usage: ./db-manage.sh [backup|restore|reset]"
            echo ""
            echo "Commands:"
            echo "  backup          - Create database backup"
            echo "  restore <file>  - Restore from backup file"
            echo "  reset           - Reset database (WARNING: deletes all data)"
            ;;
    esac
}


# ============================================================================
# 8. SSL RENEWAL SCRIPT
# ============================================================================
# File: ssl-renew.sh
# Usage: ./ssl-renew.sh

renew_ssl() {
    echo "========================================="
    echo "SSL Certificate Renewal"
    echo "========================================="
    
    echo "[1/3] Renewing certificates..."
    sudo certbot renew --quiet
    
    echo "[2/3] Testing configuration..."
    sudo nginx -t
    
    echo "[3/3] Reloading Nginx..."
    sudo systemctl reload nginx
    
    echo "========================================="
    echo "SSL renewal completed!"
    echo "========================================="
    
    # Show certificate info
    sudo certbot certificates
}


# ============================================================================
# 9. PERFORMANCE MONITORING SCRIPT
# ============================================================================
# File: monitor.sh
# Usage: ./monitor.sh

monitor_performance() {
    echo "========================================="
    echo "Performance Monitoring"
    echo "========================================="
    
    while true; do
        clear
        echo "$(date)"
        echo "========================================="
        
        # CPU Usage
        echo "CPU Usage:"
        top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}'
        
        # Memory Usage
        echo ""
        echo "Memory Usage:"
        free -h | grep Mem | awk '{print $3 "/" $2}'
        
        # Disk Usage
        echo ""
        echo "Disk Usage:"
        df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}'
        
        # Active Connections
        echo ""
        echo "Active connections:"
        netstat -an | grep :80 | wc -l
        
        # Gunicorn Workers
        echo ""
        echo "Gunicorn workers:"
        ps aux | grep gunicorn | grep -v grep | wc -l
        
        # Response Time
        echo ""
        echo "API response time:"
        curl -o /dev/null -s -w "Time: %{time_total}s\n" http://localhost/api/health/
        
        echo "========================================="
        echo "Press Ctrl+C to exit"
        sleep 5
    done
}


# ============================================================================
# 10. CLEANUP SCRIPT
# ============================================================================
# File: cleanup.sh
# Usage: ./cleanup.sh

cleanup_system() {
    echo "========================================="
    echo "System Cleanup"
    echo "========================================="
    
    # Clean Python cache
    echo "[1/5] Cleaning Python cache..."
    find /var/www/library-api -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
    find /var/www/library-api -type f -name "*.pyc" -delete
    
    # Clean old logs
    echo "[2/5] Cleaning old logs..."
    find /var/log/nginx -name "*.log.*" -mtime +30 -delete
    find /var/log/gunicorn -name "*.log.*" -mtime +30 -delete
    
    # Clean old backups
    echo "[3/5] Cleaning old backups..."
    find /var/backups/library-api -name "*.sql" -mtime +30 -delete
    find /var/backups/library-api -name "*.tar.gz" -mtime +30 -delete
    
    # Clean package cache
    echo "[4/5] Cleaning package cache..."
    sudo apt autoremove -y
    sudo apt autoclean -y
    
    # Clean pip cache
    echo "[5/5] Cleaning pip cache..."
    pip cache purge 2>/dev/null || true
    
    echo "========================================="
    echo "Cleanup completed!"
    echo "========================================="
    
    # Show disk space
    df -h /
}


# ============================================================================
# MAIN MENU
# ============================================================================

show_menu() {
    echo "========================================="
    echo "Django REST API - Deployment Scripts"
    echo "========================================="
    echo "1. Full Deployment"
    echo "2. Backup System"
    echo "3. Update Application"
    echo "4. Rollback Deployment"
    echo "5. Health Check"
    echo "6. View Logs"
    echo "7. Database Management"
    echo "8. SSL Renewal"
    echo "9. Performance Monitor"
    echo "10. System Cleanup"
    echo "0. Exit"
    echo "========================================="
}

# If script is run directly
if [ "${BASH_SOURCE[0]}" -eq "${0}" ]; then
    show_menu
    read -p "Select option: " option
    
    case $option in
        1) deploy_full ;;
        2) backup_system ;;
        3) update_application ;;
        4) read -p "Enter commit hash: " hash; rollback_deployment $hash ;;
        5) health_check ;;
        6) read -p "Service (gunicorn/nginx/django/access/all): " svc; view_logs $svc ;;
        7) read -p "Action (backup/restore/reset): " act; manage_database $act ;;
        8) renew_ssl ;;
        9) monitor_performance ;;
        10) cleanup_system ;;
        0) echo "Goodbye!"; exit 0 ;;
        *) echo "Invalid option" ;;
    esac
fi