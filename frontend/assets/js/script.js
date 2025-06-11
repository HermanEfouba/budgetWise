// Global variables
let currentUser = null;
let authToken = null;
let expenseChart = null;

// API Base URL
const API_BASE_URL = 'http://localhost:8000';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkAuthStatus();
});

// Initialize application
function initializeApp() {
    // Set current date for date inputs
    const today = new Date().toISOString().split('T')[0];
    const currentMonth = new Date().toISOString().slice(0, 7);
    
    document.getElementById('revenueDate').value = today;
    document.getElementById('expenseDate').value = today;
    document.getElementById('budgetMonth').value = currentMonth;
    
    // Load categories
    loadCategories();
}

// Setup event listeners
function setupEventListeners() {
    // Login form
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Register form
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
    
    // Add revenue form
    document.getElementById('addRevenueForm').addEventListener('submit', handleAddRevenue);
    
    // Add expense form
    document.getElementById('addExpenseForm').addEventListener('submit', handleAddExpense);
    
    // Set budget form
    document.getElementById('setBudgetForm').addEventListener('submit', handleSetBudget);
}

// Check authentication status
function checkAuthStatus() {
    const token = localStorage.getItem('authToken');
    const user = localStorage.getItem('currentUser');
    
    if (token && user) {
        authToken = token;
        currentUser = JSON.parse(user);
        showDashboard();
        loadDashboardData();
    } else {
        showAuthSection();
    }
}

// Authentication functions
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    showLoading(true);
    
    try {
        const formData = new FormData();
        formData.append('email', email);
        formData.append('password', password);
        
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            currentUser = data.user;
            
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            
            showDashboard();
            loadDashboardData();
            showToast('Connexion réussie !', 'success');
        } else {
            const error = await response.json();
            showToast(error.detail || 'Erreur de connexion', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showToast('Erreur de connexion', 'error');
    } finally {
        showLoading(false);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        showToast('Les mots de passe ne correspondent pas', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })
        });
        
        if (response.ok) {
            showToast('Compte créé avec succès ! Vous pouvez maintenant vous connecter.', 'success');
            bootstrap.Modal.getInstance(document.getElementById('registerModal')).hide();
            document.getElementById('loginEmail').value = email;
        } else {
            const error = await response.json();
            showToast(error.detail || 'Erreur lors de la création du compte', 'error');
        }
    } catch (error) {
        console.error('Register error:', error);
        showToast('Erreur lors de la création du compte', 'error');
    } finally {
        showLoading(false);
    }
}

function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    authToken = null;
    currentUser = null;
    showAuthSection();
    showToast('Déconnexion réussie', 'info');
}

// UI functions
function showAuthSection() {
    document.getElementById('authSection').style.display = 'block';
    document.getElementById('dashboardSection').style.display = 'none';
    document.getElementById('loginBtn').style.display = 'block';
    document.getElementById('userMenu').style.display = 'none';
}

function showDashboard() {
    document.getElementById('authSection').style.display = 'none';
    document.getElementById('dashboardSection').style.display = 'block';
    document.getElementById('loginBtn').style.display = 'none';
    document.getElementById('userMenu').style.display = 'block';
    document.getElementById('userName').textContent = currentUser.name;
}

function showRegisterForm() {
    const registerModal = new bootstrap.Modal(document.getElementById('registerModal'));
    registerModal.show();
}

function showLoginModal() {
    // This function can be used if you want a login modal instead of the main form
}

// Modal functions
function showAddRevenueModal() {
    const modal = new bootstrap.Modal(document.getElementById('addRevenueModal'));
    modal.show();
}

function showAddExpenseModal() {
    const modal = new bootstrap.Modal(document.getElementById('addExpenseModal'));
    modal.show();
}

function showSetBudgetModal() {
    const modal = new bootstrap.Modal(document.getElementById('setBudgetModal'));
    modal.show();
}

function showAddTransactionModal() {
    // You can implement a combined transaction modal here
    showAddExpenseModal();
}

function showReportsModal() {
    // Implement reports modal
    showToast('Fonctionnalité des rapports en cours de développement', 'info');
}

// Data loading functions
async function loadDashboardData() {
    if (!authToken) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/budgets/dashboard`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            updateDashboardStats(data);
            loadRecentTransactions();
            updateExpenseChart(data.top_categories);
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function updateDashboardStats(data) {
    document.getElementById('currentBalance').textContent = `€${data.current_balance.toFixed(2)}`;
    document.getElementById('monthlyRevenue').textContent = `€${data.total_revenue_this_month.toFixed(2)}`;
    document.getElementById('monthlyExpenses').textContent = `€${data.total_expenses_this_month.toFixed(2)}`;
    document.getElementById('budgetRemaining').textContent = `€${data.budget_remaining.toFixed(2)}`;
}

async function loadRecentTransactions() {
    if (!authToken) return;
    
    try {
        // Load recent expenses
        const expensesResponse = await fetch(`${API_BASE_URL}/expenses?limit=5`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        // Load recent revenues
        const revenuesResponse = await fetch(`${API_BASE_URL}/revenues?limit=5`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (expensesResponse.ok && revenuesResponse.ok) {
            const expenses = await expensesResponse.json();
            const revenues = await revenuesResponse.json();
            
            displayRecentTransactions([...expenses, ...revenues]);
        }
    } catch (error) {
        console.error('Error loading recent transactions:', error);
    }
}

function displayRecentTransactions(transactions) {
    const container = document.getElementById('recentTransactions');
    container.innerHTML = '';
    
    // Sort by date (most recent first)
    transactions.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    transactions.slice(0, 5).forEach(transaction => {
        const isExpense = transaction.hasOwnProperty('description');
        const item = document.createElement('div');
        item.className = 'list-group-item d-flex justify-content-between align-items-center';
        
        item.innerHTML = `
            <div>
                <div class="fw-medium">${isExpense ? transaction.description : transaction.source}</div>
                <small class="text-muted">${new Date(transaction.date).toLocaleDateString('fr-FR')}</small>
            </div>
            <span class="badge ${isExpense ? 'bg-danger' : 'bg-success'} rounded-pill">
                ${isExpense ? '-' : '+'}€${transaction.amount.toFixed(2)}
            </span>
        `;
        
        container.appendChild(item);
    });
}

async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories`);
        
        if (response.ok) {
            const categories = await response.json();
            const select = document.getElementById('expenseCategory');
            
            select.innerHTML = '<option value="">Sélectionner une catégorie</option>';
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.id;
                option.textContent = category.name;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Chart functions
function updateExpenseChart(categoryData) {
    const ctx = document.getElementById('expenseChart').getContext('2d');
    
    if (expenseChart) {
        expenseChart.destroy();
    }
    
    const labels = categoryData.map(item => item.category_name);
    const data = categoryData.map(item => item.total_amount);
    const colors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ];
    
    expenseChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors.slice(0, data.length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            }
        }
    });
}

// Form handlers
async function handleAddRevenue(e) {
    e.preventDefault();
    
    const amount = parseFloat(document.getElementById('revenueAmount').value);
    const source = document.getElementById('revenueSource').value;
    const date = document.getElementById('revenueDate').value;
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/revenues/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                amount: amount,
                source: source,
                date: date
            })
        });
        
        if (response.ok) {
            showToast('Revenu ajouté avec succès !', 'success');
            bootstrap.Modal.getInstance(document.getElementById('addRevenueModal')).hide();
            document.getElementById('addRevenueForm').reset();
            loadDashboardData();
        } else {
            const error = await response.json();
            showToast(error.detail || 'Erreur lors de l\'ajout du revenu', 'error');
        }
    } catch (error) {
        console.error('Error adding revenue:', error);
        showToast('Erreur lors de l\'ajout du revenu', 'error');
    } finally {
        showLoading(false);
    }
}

async function handleAddExpense(e) {
    e.preventDefault();
    
    const amount = parseFloat(document.getElementById('expenseAmount').value);
    const description = document.getElementById('expenseDescription').value;
    const categoryId = parseInt(document.getElementById('expenseCategory').value);
    const type = document.getElementById('expenseType').value;
    const date = document.getElementById('expenseDate').value;
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/expenses/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                amount: amount,
                description: description,
                category_id: categoryId,
                type: type,
                date: date
            })
        });
        
        if (response.ok) {
            showToast('Dépense ajoutée avec succès !', 'success');
            bootstrap.Modal.getInstance(document.getElementById('addExpenseModal')).hide();
            document.getElementById('addExpenseForm').reset();
            loadDashboardData();
        } else {
            const error = await response.json();
            showToast(error.detail || 'Erreur lors de l\'ajout de la dépense', 'error');
        }
    } catch (error) {
        console.error('Error adding expense:', error);
        showToast('Erreur lors de l\'ajout de la dépense', 'error');
    } finally {
        showLoading(false);
    }
}

async function handleSetBudget(e) {
    e.preventDefault();
    
    const month = document.getElementById('budgetMonth').value;
    const amount = parseFloat(document.getElementById('budgetAmount').value);
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/budgets/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                month: month,
                amount: amount
            })
        });
        
        if (response.ok) {
            showToast('Budget défini avec succès !', 'success');
            bootstrap.Modal.getInstance(document.getElementById('setBudgetModal')).hide();
            document.getElementById('setBudgetForm').reset();
            loadDashboardData();
        } else {
            const error = await response.json();
            showToast(error.detail || 'Erreur lors de la définition du budget', 'error');
        }
    } catch (error) {
        console.error('Error setting budget:', error);
        showToast('Erreur lors de la définition du budget', 'error');
    } finally {
        showLoading(false);
    }
}

// Utility functions
function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (show) {
        spinner.classList.remove('d-none');
    } else {
        spinner.classList.add('d-none');
    }
}

function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    const toastId = 'toast-' + Date.now();
    
    const bgClass = {
        'success': 'bg-success',
        'error': 'bg-danger',
        'warning': 'bg-warning',
        'info': 'bg-info'
    }[type] || 'bg-info';
    
    const iconClass = {
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-circle',
        'warning': 'fas fa-exclamation-triangle',
        'info': 'fas fa-info-circle'
    }[type] || 'fas fa-info-circle';
    
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="${iconClass} me-2"></i>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 5000
    });
    
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}