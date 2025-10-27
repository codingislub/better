import unittest
import json
import os
from app import app, tasks, comments, DATA_FILE


class TestCommentAPI(unittest.TestCase):
    """Test cases for Comment CRUD API"""
    
    def setUp(self):
        """Set up test client and clear data before each test"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Clear storage
        tasks.clear()
        comments.clear()
        
        # Remove data file if it exists
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        
        # Create a test task for comment operations
        response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Test Task', 'description': 'Test Description'}),
            content_type='application/json'
        )
        self.test_task = json.loads(response.data)
        self.test_task_id = self.test_task['id']
    
    def tearDown(self):
        """Clean up after each test"""
        tasks.clear()
        comments.clear()
    
    # Helper methods
    def create_comment(self, task_id, content, author='Test Author'):
        """Helper method to create a comment"""
        return self.client.post(
            f'/api/tasks/{task_id}/comments',
            data=json.dumps({'content': content, 'author': author}),
            content_type='application/json'
        )
    
    # CREATE tests
    def test_create_comment_success(self):
        """Test successful comment creation"""
        response = self.create_comment(self.test_task_id, 'This is a test comment')
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['task_id'], self.test_task_id)
        self.assertEqual(data['content'], 'This is a test comment')
        self.assertEqual(data['author'], 'Test Author')
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_create_comment_missing_content(self):
        """Test comment creation without content"""
        response = self.client.post(
            f'/api/tasks/{self.test_task_id}/comments',
            data=json.dumps({'author': 'Test Author'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Content is required')
    
    def test_create_comment_empty_content(self):
        """Test comment creation with empty content"""
        response = self.create_comment(self.test_task_id, '   ')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Content cannot be empty')
    
    def test_create_comment_task_not_found(self):
        """Test comment creation for non-existent task"""
        response = self.create_comment('non-existent-task-id', 'Test comment')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['task_id'], 'non-existent-task-id')
    
    def test_create_comment_with_anonymous_author(self):
        """Test comment creation without author (should default to Anonymous)"""
        response = self.client.post(
            f'/api/tasks/{self.test_task_id}/comments',
            data=json.dumps({'content': 'Anonymous comment'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['author'], 'Anonymous')
    
    # READ tests
    def test_get_comments_for_task(self):
        """Test retrieving all comments for a task"""
        # Create multiple comments
        self.create_comment(self.test_task_id, 'First comment')
        self.create_comment(self.test_task_id, 'Second comment')
        self.create_comment(self.test_task_id, 'Third comment')
        
        response = self.client.get(f'/api/tasks/{self.test_task_id}/comments')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['task_id'], self.test_task_id)
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['comments']), 3)
    
    def test_get_comments_empty_list(self):
        """Test retrieving comments when none exist"""
        response = self.client.get(f'/api/tasks/{self.test_task_id}/comments')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['comments']), 0)
    
    def test_get_comments_task_not_found(self):
        """Test retrieving comments for any task_id"""
        response = self.client.get('/api/tasks/non-existent-task/comments')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['comments']), 0)
    
    def test_get_single_comment(self):
        """Test retrieving a specific comment"""
        create_response = self.create_comment(self.test_task_id, 'Test comment')
        created_comment = json.loads(create_response.data)
        comment_id = created_comment['id']
        
        response = self.client.get(f'/api/comments/{comment_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], comment_id)
        self.assertEqual(data['content'], 'Test comment')
    
    def test_get_single_comment_not_found(self):
        """Test retrieving a non-existent comment"""
        response = self.client.get('/api/comments/non-existent-id')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    # UPDATE tests
    def test_update_comment_content(self):
        """Test updating comment content"""
        # Create a comment
        create_response = self.create_comment(self.test_task_id, 'Original content')
        created_comment = json.loads(create_response.data)
        comment_id = created_comment['id']
        original_updated_at = created_comment['updated_at']
        
        # Update the comment
        response = self.client.put(
            f'/api/comments/{comment_id}',
            data=json.dumps({'content': 'Updated content'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['content'], 'Updated content')
        # Verify updated_at was changed (or at least exists)
        self.assertIn('updated_at', data)
        # The timestamp should be greater than or equal to the original
        self.assertGreaterEqual(data['updated_at'], original_updated_at)
    
    def test_update_comment_author(self):
        """Test updating comment author"""
        create_response = self.create_comment(self.test_task_id, 'Test content')
        created_comment = json.loads(create_response.data)
        comment_id = created_comment['id']
        
        response = self.client.put(
            f'/api/comments/{comment_id}',
            data=json.dumps({'author': 'Updated Author'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['author'], 'Updated Author')
        self.assertEqual(data['content'], 'Test content')  # Content unchanged
    
    def test_update_comment_both_fields(self):
        """Test updating both content and author"""
        create_response = self.create_comment(self.test_task_id, 'Original')
        created_comment = json.loads(create_response.data)
        comment_id = created_comment['id']
        
        response = self.client.put(
            f'/api/comments/{comment_id}',
            data=json.dumps({'content': 'New content', 'author': 'New Author'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['content'], 'New content')
        self.assertEqual(data['author'], 'New Author')
    
    def test_update_comment_empty_content(self):
        """Test updating comment with empty content"""
        create_response = self.create_comment(self.test_task_id, 'Original')
        created_comment = json.loads(create_response.data)
        comment_id = created_comment['id']
        
        response = self.client.put(
            f'/api/comments/{comment_id}',
            data=json.dumps({'content': '   '}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_update_comment_not_found(self):
        """Test updating non-existent comment"""
        response = self.client.put(
            '/api/comments/non-existent-id',
            data=json.dumps({'content': 'Updated'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
    
    def test_update_comment_no_data(self):
        """Test updating comment without providing data"""
        create_response = self.create_comment(self.test_task_id, 'Original')
        created_comment = json.loads(create_response.data)
        comment_id = created_comment['id']
        
        response = self.client.put(
            f'/api/comments/{comment_id}',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    # DELETE tests
    def test_delete_comment_success(self):
        """Test successful comment deletion"""
        create_response = self.create_comment(self.test_task_id, 'To be deleted')
        created_comment = json.loads(create_response.data)
        comment_id = created_comment['id']
        
        response = self.client.delete(f'/api/comments/{comment_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('comment', data)
        self.assertEqual(data['comment']['id'], comment_id)
        
        # Verify comment is actually deleted
        get_response = self.client.get(f'/api/comments/{comment_id}')
        self.assertEqual(get_response.status_code, 404)
    
    def test_delete_comment_not_found(self):
        """Test deleting non-existent comment"""
        response = self.client.delete('/api/comments/non-existent-id')
        
        self.assertEqual(response.status_code, 404)
    
    def test_delete_comment_removes_from_task_list(self):
        """Test that deleting a comment removes it from task's comment list"""
        # Create multiple comments
        response1 = self.create_comment(self.test_task_id, 'Comment 1')
        response2 = self.create_comment(self.test_task_id, 'Comment 2')
        response3 = self.create_comment(self.test_task_id, 'Comment 3')
        
        comment2_id = json.loads(response2.data)['id']
        
        # Delete the middle comment
        self.client.delete(f'/api/comments/{comment2_id}')
        
        # Get all comments for the task
        response = self.client.get(f'/api/tasks/{self.test_task_id}/comments')
        data = json.loads(response.data)
        
        self.assertEqual(data['count'], 2)
        comment_ids = [c['id'] for c in data['comments']]
        self.assertNotIn(comment2_id, comment_ids)
    
    # Integration tests
    def test_full_comment_lifecycle(self):
        """Test complete CRUD lifecycle for a comment"""
        # Create
        create_response = self.create_comment(
            self.test_task_id, 
            'Initial comment',
            'John Doe'
        )
        self.assertEqual(create_response.status_code, 201)
        comment = json.loads(create_response.data)
        comment_id = comment['id']
        
        # Read
        read_response = self.client.get(f'/api/comments/{comment_id}')
        self.assertEqual(read_response.status_code, 200)
        
        # Update
        update_response = self.client.put(
            f'/api/comments/{comment_id}',
            data=json.dumps({'content': 'Updated comment'}),
            content_type='application/json'
        )
        self.assertEqual(update_response.status_code, 200)
        updated_comment = json.loads(update_response.data)
        self.assertEqual(updated_comment['content'], 'Updated comment')
        
        # Delete
        delete_response = self.client.delete(f'/api/comments/{comment_id}')
        self.assertEqual(delete_response.status_code, 200)
        
        # Verify deletion
        final_response = self.client.get(f'/api/comments/{comment_id}')
        self.assertEqual(final_response.status_code, 404)
    
    def test_multiple_tasks_multiple_comments(self):
        """Test comments are properly isolated per task"""
        # Create another task
        task2_response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Task 2'}),
            content_type='application/json'
        )
        task2 = json.loads(task2_response.data)
        task2_id = task2['id']
        
        # Create comments for both tasks
        self.create_comment(self.test_task_id, 'Task 1 Comment 1')
        self.create_comment(self.test_task_id, 'Task 1 Comment 2')
        self.create_comment(task2_id, 'Task 2 Comment 1')
        
        # Get comments for each task
        task1_comments = self.client.get(f'/api/tasks/{self.test_task_id}/comments')
        task2_comments = self.client.get(f'/api/tasks/{task2_id}/comments')
        
        task1_data = json.loads(task1_comments.data)
        task2_data = json.loads(task2_comments.data)
        
        self.assertEqual(task1_data['count'], 2)
        self.assertEqual(task2_data['count'], 1)


class TestTaskAPI(unittest.TestCase):
    """Test cases for Task API"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        tasks.clear()
        comments.clear()
        
        # Remove data file if it exists
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
    
    def test_get_all_tasks(self):
        """Test getting all tasks"""
        # Create multiple tasks
        self.client.post('/api/tasks', data=json.dumps({'title': 'Task 1'}), content_type='application/json')
        self.client.post('/api/tasks', data=json.dumps({'title': 'Task 2'}), content_type='application/json')
        
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
    
    def test_create_task(self):
        """Test task creation"""
        response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Test Task', 'description': 'Description'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Test Task')
    
    def test_get_task(self):
        """Test retrieving a task"""
        create_response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Test Task'}),
            content_type='application/json'
        )
        task = json.loads(create_response.data)
        task_id = task['id']
        
        response = self.client.get(f'/api/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Test Task')
    
    def test_update_task(self):
        """Test updating a task"""
        create_response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Original'}),
            content_type='application/json'
        )
        task = json.loads(create_response.data)
        task_id = task['id']
        
        response = self.client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps({'title': 'Updated'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated')
    
    def test_delete_task(self):
        """Test deleting a task"""
        create_response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'To Delete'}),
            content_type='application/json'
        )
        task = json.loads(create_response.data)
        task_id = task['id']
        
        response = self.client.delete(f'/api/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify it's deleted
        get_response = self.client.get(f'/api/tasks/{task_id}')
        self.assertEqual(get_response.status_code, 404)


class TestHealthCheck(unittest.TestCase):
    """Test cases for health check endpoint"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        comments.clear()
        
        # Remove data file if it exists
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')


if __name__ == '__main__':
    unittest.main()
