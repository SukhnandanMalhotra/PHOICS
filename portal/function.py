def doc_update(request, pk, username, template_name='portal/model_form_upload.html'):
    documents = Document.objects.order_by('-uploaded_at')
    for obj in documents:
        print(obj.id)
        if obj.id == pk and obj.user.username == request.user.username:
            updatex = get_object_or_404(Document, pk=pk)
            form = UpdateForm(request.POST or None, instance=updatex)
            if form.is_valid():
                form.save()
                return redirect(reverse('profile', kwargs={'username': username}))
            return render(request, template_name, {'form': form, 'title': 'Edit Image'})
    else:
        return render(request, 'portal/error_404.html')
